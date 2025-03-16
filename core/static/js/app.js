document.addEventListener("DOMContentLoaded", function () {
    const imageUpload = document.getElementById("image-upload");
    const diagnoseButton = document.getElementById("diagnose");
    const predictedDiseaseText = document.getElementById("predicted-disease");
    const treatmentRecommendationsText = document.getElementById("treatment-recommendations");
    const previewImage = document.getElementById("preview-image");
    const dropArea = document.getElementById("drop-area");

    // Function to get CSRF token from cookies (Only needed for Django)
    function getCSRFToken() {
        let cookies = document.cookie.split("; ");
        for (let cookie of cookies) {
            if (cookie.startsWith("csrftoken=")) {
                return cookie.split("=")[1];
            }
        }
        return "";
    }

    // Show image preview on file upload
    imageUpload.addEventListener("change", function () {
        const file = imageUpload.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewImage.classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        }
    });

    // Drag & Drop Feature
    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.classList.add("border-green-500");
    });

    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("border-green-500");
    });

    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.classList.remove("border-green-500");
        const file = event.dataTransfer.files[0];
        if (file) {
            imageUpload.files = event.dataTransfer.files;
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewImage.classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        }
    });

    

    // Function to provide treatment recommendations
    
});
function getTreatmentRecommendation(disease) {
    switch (disease) {
        case "Early Blight":
            return "1. Use fungicides containing chlorothalonil or copper sprays.\n" +
                "2. Practice crop rotation and avoid planting potatoes in the same area repeatedly.\n" +
                "3. Ensure proper plant spacing to improve air circulation and reduce humidity.";

        case "Late Blight":
            return "1. Apply fungicides like mancozeb or metalaxyl at the first sign of disease.\n" +
                "2. Remove and destroy infected plants to prevent further spread.\n" +
                "3. Avoid overhead irrigation to reduce leaf moisture and the spread of spores.";

        case "Healthy":
            return "Your potato plant is healthy! Maintain good agricultural practices such as:\n" +
                "✔ Regular watering (avoid overwatering)\n" +
                "✔ Proper soil management\n" +
                "✔ Early detection of any new symptoms";

        default:
            return "No recommendation available.";
    }
}
