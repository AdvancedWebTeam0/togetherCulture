function toggleSubMenu() {
    var submenu = document.getElementById("subitemNav");
    var triangle = document.getElementById("triangleIcon");
    if (submenu.style.display === "flex") {
        submenu.style.display = "none";
        triangle.classList.remove("rotate");
    } else {
        submenu.style.display = "flex";
        triangle.classList.add("rotate");
    }
}