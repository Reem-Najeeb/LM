document.addEventListener("DOMContentLoaded", function () {
    // Navbar Toggle
    const iconToggle = document.querySelector(".navbar-toggler");
    const header = document.querySelector("[data-header]");
    const searchShow = document.getElementById("search-nav-btn");
    const searchCloseBtn = document.getElementById("search-close-btn");
    const searchBox = document.getElementById("search-box");
    const btnCloseMessages = document.getElementById("btn_close_messages");
    const closeMessages = document.getElementById("close_messages");

    function toggleIcon() {
        const isCollapsed = iconToggle.classList.toggle("collapsed");
        iconToggle.innerHTML = isCollapsed ? `
            <svg width="25" height="25" viewBox="0 0 66 83" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M32.9997 41.8414L55.0955 63.9372C56.268 65.1097 57.8582 65.7684 59.5163 65.7684C61.1745 65.7684 62.7647 65.1097 63.9371 63.9372C65.1096 62.7647 65.7683 61.1745 65.7683 59.5164C65.7683 57.8583 65.1096 56.268 63.9371 55.0956L41.833 32.9997L63.933 10.9039C64.5133 10.3233 64.9735 9.63418 65.2874 8.87576C65.6014 8.11733 65.7629 7.3045 65.7627 6.48367C65.7625 5.66284 65.6006 4.85008 65.2863 4.09181C64.972 3.33353 64.5115 2.64459 63.9309 2.06431C63.3503 1.48403 62.6612 1.02378 61.9028 0.709844C61.1443 0.395904 60.3315 0.234421 59.5107 0.234614C58.6898 0.234808 57.8771 0.396673 57.1188 0.71097C56.3605 1.02527 55.6716 1.48584 55.0913 2.06639L32.9997 24.1622L10.9038 2.06639C10.3276 1.46919 9.63813 0.992731 8.87576 0.66482C8.11339 0.33691 7.29335 0.164112 6.46348 0.156512C5.63362 0.148912 4.81055 0.306661 4.04231 0.620554C3.27406 0.934447 2.57602 1.3982 1.98892 1.98475C1.40181 2.5713 0.937403 3.2689 0.622786 4.03685C0.308168 4.8048 0.149643 5.62772 0.156461 6.45759C0.163278 7.28746 0.335301 8.10767 0.662492 8.87034C0.989684 9.63302 1.46549 10.3229 2.06215 10.8997L24.1663 32.9997L2.06632 55.0997C1.46966 55.6766 0.993852 56.3664 0.666661 57.1291C0.339469 57.8918 0.167445 58.712 0.160627 59.5419C0.15381 60.3717 0.312335 61.1946 0.626952 61.9626C0.94157 62.7305 1.40598 63.4281 1.99308 64.0147C2.58019 64.6012 3.27823 65.065 4.04647 65.3789C4.81472 65.6928 5.63779 65.8505 6.46765 65.8429C7.29751 65.8353 8.11755 65.6625 8.87992 65.3346C9.64229 65.0067 10.3317 64.5303 10.908 63.9331L32.9997 41.8414Z" fill="#2B4254"/>
            </svg>` : `
            <svg width="25" height="25" viewBox="0 0 80 59" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M4.16667 0C3.0616 0 2.00179 0.438988 1.22039 1.22039C0.438987 2.00179 0 3.0616 0 4.16667C0 5.27174 0.438987 6.33154 1.22039 7.11294C2.00179 7.89435 3.0616 8.33333 4.16667 8.33333H75C76.1051 8.33333 77.1649 7.89435 77.9463 7.11294C78.7277 6.33154 79.1667 5.27174 79.1667 4.16667C79.1667 3.0616 78.7277 2.00179 77.9463 1.22039C77.1649 0.438988 76.1051 0 75 0H4.16667ZM0 29.1667C0 28.0616 0.438987 27.0018 1.22039 26.2204C2.00179 25.439 3.0616 25 4.16667 25H75C76.1051 25 77.1649 25.439 77.9463 26.2204C78.7277 27.0018 79.1667 28.0616 79.1667 29.1667C79.1667 30.2717 78.7277 31.3315 77.9463 32.1129C77.1649 32.8943 76.1051 33.3333 75 33.3333H4.16667C3.0616 33.3333 2.00179 32.8943 1.22039 32.1129C0.438987 31.3315 0 30.2717 0 29.1667ZM0 54.1708C0 53.0658 0.438987 52.006 1.22039 51.2246C2.00179 50.4432 3.0616 50.0042 4.16667 50.0042H75C76.1051 50.0042 77.1649 50.4432 77.9463 51.2246C78.7277 52.006 79.1667 53.0658 79.1667 54.1708C79.1667 55.2759 78.7277 56.3357 77.9463 57.1171C77.1649 57.8985 76.1051 58.3375 75 58.3375H4.16667C3.0616 58.3375 2.00179 57.8985 1.22039 57.1171C0.438987 56.3357 0 55.2759 0 54.1708Z" fill="#2B4254"/>
            </svg>`;
    }

    function toggleSearchBox(show) {
        searchBox.classList.toggle("active", show);
    }

    function handleScroll() {
        header.classList.toggle("active", window.scrollY > 100);
    }

    function hideMessage() {
        closeMessages.classList.add("hide");
    }

    function showMessage() {
        closeMessages.classList.remove("hide");
        setTimeout(hideMessage, 5000);
    }

    // Event Listeners
    iconToggle.addEventListener("click", toggleIcon);
    window.addEventListener("scroll", handleScroll);
    searchShow.addEventListener("click", () => toggleSearchBox(true));
    searchCloseBtn.addEventListener("click", () => toggleSearchBox(false));
    btnCloseMessages.addEventListener("click", hideMessage);

    showMessage(); 
    // إظهار الرسالة تلقائياً عند التحميل
});

// Rate
function updateStars(container, rating) {
    const stars = container.querySelectorAll('.star');
    stars.forEach(star => {
        const starValue = parseFloat(star.getAttribute('data-value'));
        if (starValue <= rating) {
            star.innerHTML = '&#9733;'; // ★ نجمة ممتلئة
            star.classList.add('filled');
            star.classList.remove('empty');
        } else {
            star.innerHTML = '&#9734;'; // ☆ نجمة مفرغة
            star.classList.remove('filled');
            star.classList.add('empty');
        }
    });
}






