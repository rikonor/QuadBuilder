// This adds any item from the parts list when you click on it
$(document).on('click','.itemPartsList', function() {
    var itemType = $(this)[0].getElementsByClassName('itemId')[0].id
    var itemId   = $(this)[0].getElementsByClassName('itemId')[0].textContent
    var itemText = $(this)[0].getElementsByClassName('itemText')[0].textContent
    var item = $('#finalList #'+itemType)[0]
    item.innerHTML = "<span class='itemId'>"+itemId+"</span><span class='itemText'>"+itemText+"</span>"
});

// This removes any item from the final list when you click on it.
$(document).on('click','.itemFinalList', function() {
    $(this)[0].innerHTML = ""
});

$(document).on('click','#reset', function() {
    $('.itemFinalList').each(function() {
        $(this)[0].innerHTML = ""
    });
});

// This event handler submits the build spec provided by the user
$(document).on('click','#submit', function() {
    //This function has a bug!!! If user did not select a part, it will give an error.
    var motorId = $('#finalList #Motor')[0].getElementsByClassName('itemId')[0].textContent
    var escId   = $('#finalList #Esc')[0].getElementsByClassName('itemId')[0].textContent
    var propId  = $('#finalList #Prop')[0].getElementsByClassName('itemId')[0].textContent
    $('<form action="/AddSpec" method="POST">' + 
    '<input type="hidden" name="motorId" value="' + motorId + '">' +
    '<input type="hidden" name="escId" value="' + escId   + '">' +
    '<input type="hidden" name="propId" value="' + propId  + '">' +
    '</form>').submit();
});

// This takes the user to the Add page if he clicks the Add button on the main page.
$(document).on('click','#add', function() {
    window.location.href = "/Add";
});

// Tabs logic.  From (http://www.my-html-codes.com/javascript-tabs-html-5-css3)
window.onload=function() {

  // get tab container
  var container = document.getElementById("tabContainer");
    // set current tab
    var navitem = container.querySelector(".tabs ul li");
    //store which tab we are on
    var ident = navitem.id.split("_")[1];
    navitem.parentNode.setAttribute("data-current",ident);
    //set current tab with class of activetabheader
    navitem.setAttribute("class","tabActiveHeader");

    //hide two tab contents we don't need
    var pages = container.querySelectorAll(".tabpage");
    for (var i = 1; i < pages.length; i++) {
      pages[i].style.display="none";
    }

    //this adds click event to tabs
    var tabs = container.querySelectorAll(".tabs ul li");
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].onclick=displayPage;
    }
}

// on click of one of tabs
function displayPage() {
  var current = this.parentNode.getAttribute("data-current");
  //remove class of activetabheader and hide old contents
  document.getElementById("tabHeader_" + current).removeAttribute("class");
  document.getElementById("tabpage_" + current).style.display="none";

  var ident = this.id.split("_")[1];
  //add class of activetabheader to new active tab and show contents
  this.setAttribute("class","tabActiveHeader");
  document.getElementById("tabpage_" + ident).style.display="block";
  this.parentNode.setAttribute("data-current",ident);
}