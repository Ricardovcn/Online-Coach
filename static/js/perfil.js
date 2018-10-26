var req = new XMLHttpRequest;

var corpoVideos = document.getElementById("video");

function requisicao(){
    req.open("GET", "https://www.googleapis.com/youtube/v3/search?part=id&order=relevance&q="+corpoVideos.value+"&key=AIzaSyDrcUdUEc-7E_QqCh9GTBry4zfh3An5SWg");
    req.send(null);
}

function exibirInformacoes() {
  var resp = req.responseText;
  var resp_obj = JSON.parse(resp);

  corpoVideos.innerHTML = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+resp_obj['items'][1]['id']['videoId']+'" frameborder="0" encrypted-media" allowfullscreen></iframe><br><br>';

}

req.onloadend = exibirInformacoes

$( document ).ready(function() {
    requisicao()
});