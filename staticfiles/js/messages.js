document.addEventListener("DOMContentLoaded", function () {
    const closeButtons = document.querySelectorAll(".close-message");
    
    closeButtons.forEach((btn) => {
        btn.addEventListener("click", function () {
            const messageId = this.getAttribute("data-id");
            const messageBox = document.getElementById(messageId);
            if (messageBox) {
                messageBox.style.display = "none";
            }
        });
    });

    // إخفاء الرسائل تلقائيًا بعد 5 ثوانٍ
    setTimeout(() => {
        document.querySelectorAll(".messages").forEach((msg) => {
            msg.style.opacity = "0";
            setTimeout(() => msg.style.display = "none", 500);
        });
    }, 5000);
});