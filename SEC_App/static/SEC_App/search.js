
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

function openPage(evt, pageName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(pageName).style.display = "block";
    evt.currentTarget.className += " active";
  }

function openTweets(evt, pageName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tweets-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tweets-tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(pageName).style.display = "block";
    evt.currentTarget.className += " active";
  }