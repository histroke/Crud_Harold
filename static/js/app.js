function abrirModalEliminar(idProducto) {
    Swal.fire({
        title: 'Eliminar Producto',
        text: "¿Está seguro de eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'NO',
        confirmButtonText: 'SI'
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = "/eliminar/" + idProducto;
        }
    });
}


// Buscador en tiempo real para la tabla
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', (e) => {
            const text = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const productName = row.querySelector('.user-name');
                if (productName) {
                    const name = productName.textContent.toLowerCase();
                    row.style.display = name.includes(text) ? '' : 'none';
                }
            });
        });
    }
});