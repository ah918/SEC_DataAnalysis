
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

function tweets_filter(){
  var formdata = $('#filter').serializeArray();
  var dataObj = {};

  $(formdata).each(function(i, field){
    dataObj[field.name] = field.value;
  });

  var filter = dataObj['class'];

  var tables = document.getElementsByClassName("tweets-table");

  // Loop through all table rows, and hide those who don't match the search query
  for (j=0; j<tables.length; j++ ){
    var tr = tables[j].getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[2];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue == filter || filter == 'جميع المواضيع') {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}