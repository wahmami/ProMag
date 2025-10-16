import streamlit as st
from pathlib import Path
import importlib
import config as _cfg_module  # load config.py module

from settings.teachers import render as teachers_render
from settings.vacations import vacations_menu
from settings.rapports import render as rapports_render

# Helpers
def _csv_list(text: str) -> list[str]:
    return [p.strip() for p in (text or "").split(",") if p.strip()]

def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def _load_cfg() -> dict:
    # read current values from config.py
    return {
        "subjects": list(getattr(_cfg_module, "subjects", [])),
        "classes": list(getattr(_cfg_module, "classes", [])),
        "materials": list(getattr(_cfg_module, "materials", [])),
        "modules": list(getattr(_cfg_module, "modules", [])),
        "submodules": dict(getattr(_cfg_module, "submodules", {})),
    }

def _write_config(cfg: dict):
    cfg_path = _project_root() / "config.py"
    content = (
        f"subjects = {repr(cfg['subjects'])}\n"
        f"classes = {repr(cfg['classes'])}\n"
        f"materials = {repr(cfg['materials'])}\n"
        f"modules = {repr(cfg['modules'])}\n"
        f"submodules = {repr(cfg['submodules'])}\n"
    )
    cfg_path.write_text(content, encoding="utf-8")
    # reload config so UI reflects new values
    importlib.reload(_cfg_module)

def add_msg(level: str, text: str):
    (getattr(st, level) if hasattr(st, level) else st.info)(text)

def render():
    cfg = _load_cfg()
    tabs = st.tabs([
        "Teachers", "Subjects", "Classes", "Materials", "Modules", "Submodules", "Vacations", "Rapports"
    ])

    with tabs[0]:
        teachers_render()

    # Subjects
    with tabs[1]:
        st.caption("Edit subjects list (comma separated).")
        subj_text = st.text_area("Subjects", ", ".join(cfg["subjects"]), key="cfg_subjects_edit", height=120)
        if st.button("Save Subjects", key="cfg_save_subjects"):
            cfg["subjects"] = _csv_list(subj_text)
            _write_config(cfg)
            add_msg("success", "Subjects saved.")

    # Classes
    with tabs[2]:
        st.caption("Edit classes list (comma separated).")
        classes_text = st.text_area("Classes", ", ".join(cfg["classes"]), key="cfg_classes_edit", height=120)
        if st.button("Save Classes", key="cfg_save_classes"):
            cfg["classes"] = _csv_list(classes_text)
            _write_config(cfg)
            add_msg("success", "Classes saved.")

    # Materials
    with tabs[3]:
        st.caption("Edit materials list (comma separated).")
        materials_text = st.text_area("Materials", ", ".join(cfg["materials"]), key="cfg_materials_edit", height=120)
        if st.button("Save Materials", key="cfg_save_materials"):
            cfg["materials"] = _csv_list(materials_text)
            _write_config(cfg)
            add_msg("success", "Materials saved.")

    # Modules
    with tabs[4]:
        st.caption("Edit modules list (comma separated).")
        modules_text = st.text_area("Modules", ", ".join(cfg["modules"]), key="cfg_modules_edit", height=120)
        if st.button("Save Modules", key="cfg_save_modules"):
            new_modules = _csv_list(modules_text)
            # keep only submodules for existing modules
            new_submodules = {m: cfg["submodules"].get(m, []) for m in new_modules}
            cfg["modules"] = new_modules
            cfg["submodules"] = new_submodules
            _write_config(cfg)
            add_msg("success", "Modules saved. Submodules synced.")

    # Submodules
    with tabs[5]:
        if not cfg["modules"]:
            st.info("No modules defined. Add modules first.")
        else:
            st.caption("Define submodules for each module (comma separated).")
            updated_subs = {}
            for m in cfg["modules"]:
                existing = cfg["submodules"].get(m, [])
                edit = st.text_area(f"{m} submodules", ", ".join(existing), key=f"cfg_subs_{m}", height=80)
                updated_subs[m] = _csv_list(edit)
            if st.button("Save All Submodules", key="cfg_save_all_submodules"):
                cfg["submodules"] = updated_subs
                _write_config(cfg)
                add_msg("success", "Submodules saved.")

    # Vacations
    with tabs[6]:
        vacations_menu()

    msgs = []
    with tabs[7]:
        msgs += rapports_render() or []

    return msgs