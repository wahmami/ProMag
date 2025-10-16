import streamlit as st
from database import (
    create_rapport, list_rapports, delete_rapport,
    set_rapport_assignments, list_rapport_assignments,
    load_teachers,
)

def _teacher_names_only(items):
    if not items:
        return []
    x = items[0]
    if isinstance(x, dict):
        return [i.get("name", "") for i in items]
    if isinstance(x, (list, tuple)):
        return [i[1] for i in items]
    return [str(i) for i in items]

def render():
    messages = []
    def add_msg(level, text): messages.append((level, text))

    st.subheader("Rapports")

    # Create rapport
    with st.expander("Create rapport", expanded=True):
        title = st.text_input("Title", key="settings_rp_title")
        announce = st.date_input("Announcement Date", key="settings_rp_announce")
        due = st.date_input("Due Date", key="settings_rp_due")
        teacher_list = _teacher_names_only(load_teachers() or [])
        concerned = st.multiselect("Concerned teachers", teacher_list, key="settings_rp_concerned")
        if st.button("Save Rapport", key="settings_rp_save", disabled=not (title and announce and due and concerned)):
            rid = create_rapport(title.strip(), announce.isoformat(), due.isoformat())
            set_rapport_assignments(rid, concerned)
            add_msg("success", f"Rapport created (id={rid}).")

    # Edit assignments
    with st.expander("Edit assignments", expanded=False):
        rap = list_rapports()
        if not rap:
            st.info("No rapports yet.")
        else:
            labels = [f"{r['id']} — {r['title']} (due {r['due_date']})" for r in rap]
            idx = 0 if labels else None
            sel = st.selectbox("Select rapport", labels, index=idx, key="settings_rp_edit_sel")
            r = rap[labels.index(sel)] if sel else None
            if r:
                teacher_list = _teacher_names_only(load_teachers() or [])
                current = set(list_rapport_assignments(r["id"]))
                chosen = st.multiselect(
                    "Concerned teachers",
                    teacher_list,
                    default=[t for t in teacher_list if t in current],
                    key=f"settings_rp_assign_{r['id']}"
                )
                if st.button("Save Assignments", key=f"settings_rp_assign_save_{r['id']}"):
                    set_rapport_assignments(r["id"], chosen)
                    add_msg("success", "Assignments updated.")

    # Existing rapports list with delete
    st.markdown("Existing rapports")
    rap = list_rapports()
    if not rap:
        st.info("No rapports yet.")
        return messages
    for r in rap:
        st.write(f"{r['id']} — {r['title']} (announce {r['announce_date']} | due {r['due_date']})")
        assigned = ", ".join(list_rapport_assignments(r["id"]) or [])
        if assigned:
            st.caption(f"Assigned: {assigned}")
        if st.button(f"Delete {r['id']}", key=f"settings_rp_del_{r['id']}"):
            delete_rapport(r["id"])
            add_msg("success", f"Rapport {r['id']} deleted.")
            st.rerun()

    return messages