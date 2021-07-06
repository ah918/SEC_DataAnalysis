
function keywords(){
    var text = document.getElementById('keyword').value;
    var text_list = text.split(' ');

    var or_and = document.getElementById('or_and');
    if (text_list.length>1){
        or_and.style.display = 'inline-block';
    }
    else {
        or_and.style.display = 'none';
    }
    
    var keyword_option = document.getElementById('keyword_option');
    if (text.length>1){
        keyword_option.style.display = 'inline-block';
    }
    else {
        keyword_option.style.display = 'none';
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


