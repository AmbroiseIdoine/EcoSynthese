$(document).ready(function() {
    $("cause_text").hide();
    $(".diagram_text").hide();
    $(".secteur_description").hide();
});
function show_text(id){
    document.getElementById(id).style.display = 'block';
}
function hide_text(id){
    document.getElementById(id).style.display = 'none';
}