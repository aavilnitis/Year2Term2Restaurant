window.onload = function() {
    var userTypeDropdown = document.getElementById("user_type");
    var waiterFields = document.getElementById("waiter_fields");
    var kitchenFields = document.getElementById("kitchen_fields");
  
    userTypeDropdown.addEventListener("change", function() {
      if (userTypeDropdown.value === "waiter") {
        waiterFields.style.display = "block";
        kitchenFields.style.display = "none";
      } else if (userTypeDropdown.value === "kitchen") {
        waiterFields.style.display = "none";
        kitchenFields.style.display = "block";
      } else {
        waiterFields.style.display = "none";
        kitchenFields.style.display = "none";
      }
    });
  };
  