$(document).ready(function() {
    $(".diagram_text").hide()
});
function show_text(id){
    document.getElementById(id).style.display = 'block';
}
function hide_text(id){
    document.getElementById(id).style.display = 'none';
}