var buttons = document.getElementsByClassName("update-cart");
var min_count_of_product = 0;
var max_count_of_product = 10;

for (i = 0; i < buttons.length; i++){
    buttons[i].addEventListener('click', function() {
        if (this.dataset.type_of_button == "add_to_chart"){
            count_input = document.querySelectorAll(`[data-id_of_count='${this.dataset.product}.count']`)[0];
            count_input.innerText = Number(count_input.innerText)+1
            hide = document.querySelectorAll(`[data-id_of_count='${this.dataset.product}.add']`)[0];
            show = document.querySelectorAll(`[data-id_of_count='${this.dataset.product}.plus_minus_div']`)[0];
            replace(hide, show);
        } else {
            count_input = document.querySelectorAll(`[data-id_of_count='${this.dataset.product}.count']`)[0];
            if (this.innerText == '-'){
                count_input.innerText = Number(count_input.innerText)-1;
                if (Number(count_input.innerText)<=0) {
                    hide = document.querySelectorAll(`[data-id_of_count='${this.dataset.product}.plus_minus_div']`)[0];
                    show = document.querySelectorAll(`[data-id_of_count='${this.dataset.product}.add']`)[0];
                    replace(hide, show)
                }
            } else {
                count_input.innerText = Number(count_input.innerText)+1
            };
        };
        if (this.value > max_count_of_product){
            count_input.value = max_count_of_product
        } else if (this.value < min_count_of_product) {
            count_input.value = min_count_of_product
        };
    });
};

function replace( hide, show ) {
    hide.style.display="none";
    show.style.display="block";
};