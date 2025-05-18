/* Called:
contactUs.html , 
*/
// main all fildes ****************
function validateField(error, inputElement) {
    if (inputElement && inputElement.value.trim() === '') {
        error.classList.add("invalid");
        return false;
    } else {
        error.classList.remove("invalid");
        return true;
    }
}
// main all fildes call
function runValidateAllFields() {
    const fieldContainers = document.querySelectorAll(".filde-container");
    let isValid = true;

    fieldContainers.forEach(container => {
        const errorfield = container.querySelector(".invalid-feedback");
        const inputfield = container.querySelector(".form-control");

        if (!validateField(errorfield, inputfield)) {
            isValid = false;
        }
    });
    return isValid;
}
// main all auto fildes
function autoVaildfillFildes(){
    const fieldContainers = document.querySelectorAll(".filde-container");

    fieldContainers.forEach(container => {
        const inputField = container.querySelector(".form-control");
        const errorField = container.querySelector(".invalid-feedback");

        // عند الكتابة داخل الحقل، يتم التحقق من صحة المدخل
        inputField.addEventListener("input", function () {
            validateField(errorField, inputField);
        });
    });
}

// main Email ****************
function validateEmail(error, inputEmail) {
    // التأكد من أن البريد ينتهي بـ "@gmail.com" وعدم وجود مسافات
    const emailPattern = /^[^ ]+@gmail\.com$/;
    if (!inputEmail.value.trim().match(emailPattern)) {
        error.classList.add("invalid");
        return false;
    }
    error.classList.remove("invalid");
    return true;
}

function runValidateEmail() {
    // تحديد حاوية البريد الإلكتروني التي تحتوي على كلا من حقل الإدخال وعنصر الخطأ
    const container = document.querySelector(".email");
    if (!container) return true; // إذا لم يوجد عنصر البريد، نفترض أن التحقق صحيح
    const inputField = container.querySelector(".form-control");
    const errorField = container.querySelector(".invalid-feedback");
    return validateEmail(errorField, inputField);
}

function autoVaildEmail(){
    const emailContainer = document.querySelector(".email");
    if (emailContainer) {
        const emailInput = emailContainer.querySelector(".form-control");
        const emailError = emailContainer.querySelector(".invalid-feedback");
        emailInput.addEventListener("input", () => {
            validateEmail(emailError, emailInput);
        });
    }
}

// Phone Number ****************
// دالة تنقية تُبقي على الأرقام فقط
function filterToNumbers(inputElement) {
    inputElement.value = inputElement.value.replace(/\D/g, ''); // إزالة كل شيء غير رقمي
}

// دالة التحقق من رقم الهاتف
function validatePhoneInput(inputElement, errorElement) {
    // إزالة المسافات الزائدة
    const phoneValue = inputElement.value.trim();
    const phonePattern = /^[7-9][0-9]{8}$/; // الرقم يجب أن يبدأ من 7 إلى 9 ثم يتبعه 8 أرقام

    if (!phoneValue.match(phonePattern)) {
        errorElement.classList.add("invalid"); // إضافة خطأ إذا كان الرقم غير صالح
        return false;
    }
    errorElement.classList.remove("invalid"); // إزالة الخطأ إذا كان الرقم صحيحًا
    return true;
}

// دالة لتشغيل التحقق على رقم الهاتف عند الكتابة أو عند تقديم النموذج
function runValidatePhoneInput() {
    const phoneContainer = document.querySelector(".phone"); // حاوية رقم الهاتف
    if (!phoneContainer) return false; // إذا لم توجد الحاوية، لا نقوم بأي شيء

    const inputField = phoneContainer.querySelector(".form-control"); // حقل الإدخال
    const errorField = phoneContainer.querySelector(".invalid-feedback"); // عنصر رسالة الخطأ

    // إذا كانت الحقول موجودة، نقوم بتصفية المدخلات ثم التحقق
    if (inputField && errorField) {
        filterToNumbers(inputField); // تنقية المدخلات
        return validatePhoneInput(inputField, errorField); // التحقق من رقم الهاتف
    }
    return true;
}

function restrictToEnglish(inputField) {
    const value = inputField.value;

    // السماح فقط للأحرف الإنجليزية، الأرقام، الرموز، والمسافات
    const regex = /^[A-Za-z0-9\s!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/;

    // إذا كانت القيمة تحتوي على أحرف غير مسموح بها، قم بإزالتها
    if (!regex.test(value)) {
        inputField.value = value.replace(/[^A-Za-z0-9\s!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/g, '');
    }
}
// دالة للتحقق من قوة كلمة المرور
function validatePassword() {
    const passwordInput = document.getElementById("password");
    const passwordFeedback = document.querySelector(".password .invalid-feedback");

    passwordInput.addEventListener("input", function () {
        const password = passwordInput.value;
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        let message = "";

        if (password.length === 0) {
            message = "الرجاء إدخال كلمة مرور صالحة";
        } else if (password.length < minLength) {
            message = "يجب أن تكون كلمة المرور أكثر من 8 أحرف.";
        } else if (!hasUpperCase) {
            message = "يجب أن تحتوي على حرف كبير واحد على الأقل.";
        } else if (!hasLowerCase) {
            message = "يجب أن تحتوي على حرف صغير واحد على الأقل.";
        } else if (!hasNumber) {
            message = "يجب أن تحتوي على رقم واحد على الأقل.";
        } else if (!hasSpecialChar) {
            message = "يجب أن تحتوي على رمز خاص واحد على الأقل (!@#$%^&*).";
        }

        if (message) {
            passwordFeedback.textContent = message;
            passwordFeedback.classList.add("invalid");
            passwordFeedback.style.display = "block";
        } else {
            passwordFeedback.classList.remove("invalid");
            passwordFeedback.style.display = "none";
        }
    });
}

// دالة للتحقق من تطابق كلمة المرور مع تأكيد كلمة المرور
function validateConfirmPassword() {
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const confirmFeedback = document.querySelector(".confirm-password .invalid-feedback");

    confirmPasswordInput.addEventListener("input", function () {
        if (confirmPasswordInput.value.length === 0) {
            confirmFeedback.textContent = "الرجاء تأكيد كلمة المرور.";
            confirmPasswordInput.classList.add("invalid");
            confirmFeedback.style.display = "block";
        } else if (confirmPasswordInput.value !== passwordInput.value) {
            confirmFeedback.textContent = "كلمة المرور غير متطابقة!";
            confirmPasswordInput.classList.add("invalid");
            confirmFeedback.style.display = "block";
        } else {
            confirmPasswordInput.classList.remove("invalid");
            confirmFeedback.style.display = "none";
        }
    });
}

// SignUp.html => استدعاء الدوال عند تحميل الصفحة
/*
document.addEventListener("DOMContentLoaded", function () {
    validatePassword();
    validateConfirmPassword();
});
*/
// البحث عن جميع الحقول التي تحتوي على الكلاس "en" ومنع الأحرف غير المسموح بها
window.onload = function () {
    const englishFields = document.querySelectorAll('.en');

    englishFields.forEach(field => {
        field.addEventListener('input', () => restrictToEnglish(field));
    });
};


// عند تحميل الصفحة يتم إضافة مستمعي الأحداث على حقول الإدخال
document.addEventListener("DOMContentLoaded", () => {
    autoVaildfillFildes();
    // // SignUp.html & SignIn.html & forgetpass.html => autoVaildEmail();
});

// السماح فقط للأحرف الإنجليزية والمسافة

/*
 <script>
        // استهداف حقل الهاتف أثناء الكتابة +++++++
        const phoneInput = document.getElementById("phone");
        if (phoneInput) {
            phoneInput.addEventListener("input", function () {
                runValidatePhoneInput(); // استدعاء التحقق أثناء الكتابة
            });
        }



        const form = document.getElementById("contactForm");
        form.addEventListener("submit", (e) => {
            // نفترض أن runValidateAllFields() مُعرفة مسبقاً وتتحقق من باقي الحقول
            if (!runValidateAllFields() || !runValidateEmail() || !runValidatePhoneInput()) {
                e.preventDefault();
                console.log('تم منع إرسال النموذج لوجود أخطاء.');
            }
            // إذا كانت جميع الحقول صحيحة، يتم إرسال النموذج تلقائيًا
        });

</script>
 */


//  ****************

//  ****************
//  ****************
//  ****************
// Form ****************




