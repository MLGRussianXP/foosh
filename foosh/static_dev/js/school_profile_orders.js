document.addEventListener("DOMContentLoaded", function() {
    const orderItems = document.querySelectorAll(".order-item-info");
  
    orderItems.forEach(function(item) {
      item.addEventListener("click", function() {
        const details = this.parentNode.querySelectorAll(".order-item-detail");
        details.forEach(detail => {
          detail.style.display = detail.style.display === "none" ? "block" : "none";
        });
      });
    });
  });
  