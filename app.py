import streamlit as st
from typing import Dict, List


def init_state() -> None:
    if "todos" not in st.session_state:
        st.session_state.todos = []  # type: List[Dict[str, object]]
    if "new_todo" not in st.session_state:
        st.session_state.new_todo = ""


def add_todo(text: str) -> None:
    if not text.strip():
        return
    st.session_state.todos.append({"text": text.strip(), "done": False})


def submit_todo() -> None:
    add_todo(st.session_state.new_todo)
    st.session_state.new_todo = ""


def remove_todo(index: int) -> None:
    st.session_state.todos.pop(index)


def toggle_todo(index: int) -> None:
    st.session_state.todos[index]["done"] = not st.session_state.todos[index]["done"]


def main() -> None:
    st.set_page_config(page_title="할 일 관리", page_icon="✅", layout="centered")
    init_state()

    st.title("할 일(To-Do) 관리")
    st.write("Streamlit 세션 상태를 사용해 할 일을 추가하고, 완료 체크하고, 삭제하세요.")

    with st.form(key="todo_form"):
        st.text_input("새 할 일", placeholder="예: 장보기 목록 작성", key="new_todo")
        st.form_submit_button("추가", on_click=submit_todo)

    total_count = len(st.session_state.todos)
    done_count = sum(1 for item in st.session_state.todos if item["done"])
    not_done_count = total_count - done_count

    st.markdown(f"**요약**: 전체 {total_count}개, 완료 {done_count}개, 미완료 {not_done_count}개")

    if total_count == 0:
        st.info("아직 등록된 할 일이 없습니다. 위에 새 할 일을 추가해보세요.")
        return

    for index, item in enumerate(st.session_state.todos):
        cols = st.columns([0.1, 0.7, 0.2])
        checked = cols[0].checkbox("", value=item["done"], key=f"todo_{index}", on_change=toggle_todo, args=(index,))

        label = item["text"]
        if item["done"]:
            label = f"~~{label}~~"

        cols[1].markdown(label)
        if cols[2].button("삭제", key=f"delete_{index}", on_click=remove_todo, args=(index,)):
            st.experimental_rerun()


if __name__ == "__main__":
    main()
