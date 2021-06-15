Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

document.getElementById('end_date').value = new Date().toDateInputValue();

function keywords(){
    var text = document.getElementById('keyword').value;
    var text_list = text.split(' ');

    if (text_list.length>1){
        var or_and = document.getElementById('or_and');
        or_and.classList.add('show');
    }
    else {
        or_and.classList.remove('show');
    }

    if (text_list.length>1){
        var keyword_option = document.getElementById('keyword_option');
        keyword_option.classList.add('show');
    }
    else {
        keyword_option.classList.remove('show');
    }
}