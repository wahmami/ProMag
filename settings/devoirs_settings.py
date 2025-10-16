import streamlit as st
from config import classes
from database import (
    list_devoirs_scope,
    list_devoirs_teachers,
    get_devoirs_classes_for_teacher,
    set_devoirs_classes_for_teacher,
    clear_devoirs_for_teacher,
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

    st.subheader("Devoirs Scope (Teacher/Class tracking)")

    teacher_list = _teacher_names_only(load_teachers() or [])
    t_sel = st.selectbox("Teacher", teacher_list, key="dev_scope_teacher")
    current = set(get_devoirs_classes_for_teacher(t_sel)) if t_sel else set()
    chosen = st.multiselect(
        "Tracked Classes",
        classes,
        default=[c for c in classes if c in current],
        key="dev_scope_classes"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Scope for Teacher", key="dev_scope_save", disabled=not t_sel):
            set_devoirs_classes_for_teacher(t_sel, chosen)
            add_msg("success", f"Saved Devoirs scope for {t_sel}.")
    with col2:
        if st.button("Clear Teacher Scope", key="dev_scope_clear", disabled=not t_sel):
            clear_devoirs_for_teacher(t_sel)
            add_msg("success", f"Cleared Devoirs scope for {t_sel}.")

    st.markdown("Current scope")
    data = list_devoirs_scope()
    if not data:
        st.info("No Devoirs scope defined.")
        return messages

    by_teacher = {}
    for r in data:
        by_teacher.setdefault(r["teacher_name"], []).append(r["class_name"])
    for t in sorted(by_teacher):
        st.write(f"{t}: {', '.join(sorted(by_teacher[t]))}")

    return messages