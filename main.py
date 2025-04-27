from js import document, window
from pyodide.ffi import create_proxy

from pip_dev.app import check_version, generate_versions_table

# Elements:
output_el = document.getElementById("js-output")
source_el = document.getElementById("js-source")
check_el = document.getElementById("js-check")

ex0_el = document.getElementById("js-example-0")
ex1_el = document.getElementById("js-example-1")
ex2_el = document.getElementById("js-example-2")


def get_url_param(name):
    params = (
        str(window.location.search)
        .strip("?")
        .replace("%3E", ">")
        .replace("%3C", "<")
        .replace("%7E", "~")
    )
    if params == "":
        return False
    params = params.split("&")
    for param in params:
        if param.startswith(name + "="):
            param = param.lstrip(name + "=")
            if param != "":
                return param
    return False


def do_check():
    if check_el.value == "" or source_el.value == "":
        check_el.setAttribute("aria-invalid", "")
        return

    try:
        is_valid = check_version(check_el.value, source_el.value)
    except Exception:
        check_el.setAttribute("aria-invalid", "")
    else:
        check_el.setAttribute("aria-invalid", "false" if is_valid else "true")


def do_update(value):
    try:
        table_content = generate_versions_table(value, fmt="html")
    except Exception:
        source_el.setAttribute("aria-invalid", "true")
        output_el.innerHTML = ""
    else:
        if table_content.strip() == "":
            source_el.setAttribute("aria-invalid", "true")
            output_el.innerHTML = ""
        else:
            source_el.setAttribute("aria-invalid", "false")
            table_el = document.createElement("table")
            table_el.innerHTML = table_content
            table_el.classList.add("ms-table")
            output_el.innerHTML = ""
            output_el.appendChild(table_el)
    do_check()


def manage_update(e):
    do_update(e.target.value)


source_el.addEventListener("input", create_proxy(manage_update))
source_el.addEventListener("propertychange", create_proxy(manage_update))


def manage_check(e):
    do_check()


check_el.addEventListener("input", create_proxy(manage_check))
check_el.addEventListener("propertychange", create_proxy(manage_check))

ex0_el.addEventListener("click", create_proxy(lambda e: set_spec(ex0_el.textContent)))
ex1_el.addEventListener("click", create_proxy(lambda e: set_spec(ex1_el.textContent)))
ex2_el.addEventListener("click", create_proxy(lambda e: set_spec(ex2_el.textContent)))


def set_spec(value):
    source_el.value = value
    do_update(value)


def set_vers(value):
    check_el.value = value


vers = get_url_param("vers")
vers = vers if vers else "1.2.1"
set_vers(vers)

spec = get_url_param("spec")
spec = spec if spec else "~=1.2"
set_spec(spec)

source_el.focus()
body_el = document.getElementsByTagName("html")[0]
body_el.className += " is-loaded"
