// ✅ Add Product
document.getElementById('addProductForm').addEventListener('submit', async (event) => {
  event.preventDefault();

  const name = document.getElementById('productName').value;
  const description = document.getElementById('productDescription').value;
  const price = document.getElementById('productPrice').value;
  const stock = document.getElementById('productStock').value;

  const response = await fetch('/dashboard/add-product/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}'
      },
      body: JSON.stringify({ name, description, price, stock })
  });

  if (response.ok) location.reload();
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
