document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("addProductForm");

  form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const productName = document.getElementById("productName").value.trim();
      const productDescription = document.getElementById("productDescription").value.trim();
      const productPrice = document.getElementById("productPrice").value.trim();
      const productStock = document.getElementById("productStock").value.trim();

      if (!productName || !productDescription || !productPrice || !productStock) {
          displayMessage("All fields are required!", "error");
          return;
      }

      const productData = {
          name: productName,
          description: productDescription,
          price: parseFloat(productPrice),
          stock_quantity: parseInt(productStock),
      };

      try {
          const response = await fetch("/products/", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify(productData),
          });

          const result = await response.json();

          if (!response.ok) {
              throw new Error(result.error || "Failed to add product");
          }

          displayMessage("Product added successfully!", "success");

          form.reset();

          setTimeout(() => location.reload(), 1500);
      } catch (error) {
          console.error("Error:", error);
          displayMessage(`${error.message}`, "error");
      }
  });

  // Function to display messages
  function displayMessage(message, type) {
      let messageBox = document.getElementById("messageBox");

      if (!messageBox) {
          messageBox = document.createElement("div");
          messageBox.id = "messageBox";
          document.body.prepend(messageBox);
      }

      messageBox.textContent = message;
      messageBox.className = type;
      setTimeout(() => {
          messageBox.textContent = "";
          messageBox.className = "";
      }, 4000);
  }
});


// ✅ Delete Product
async function deleteProduct(productId) {
  const response = await fetch(`/dashboard/delete-product/${productId}/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': '{{ csrf_token }}' }
  });

  if (response.ok) location.reload();
}

// ✅ Edit Product
async function editProduct(productId) {
  const newName = prompt('Enter new product name:');
  if (newName) {
      const response = await fetch(`/dashboard/edit-product/${productId}/`, {
          method: 'PUT',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': '{{ csrf_token }}'
          },
          body: JSON.stringify({ name: newName })
      });

      if (response.ok) location.reload();
  }
}
