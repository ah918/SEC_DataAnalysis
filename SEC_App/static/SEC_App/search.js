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

function loadingPage(){
    div = document.getElementById('loading-wrapper');
    div.style.display = "block" ;

    h3 = document.getElementById('loading-wrapper-h3');
    h3.style.display = "block" ;

    body = document.getElementById("full-page");
    body.style.display = "none" ;

    return true;
}

function windowPrint(){
    document.querySelector("#results-page").contentWindow.print()
}