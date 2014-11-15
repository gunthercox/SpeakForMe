var $btnRecord = $('.js-btn-record');
var $btnStop = $('.js-btn-stop');

var $textSaid = $('.js-text-said');

var recorder = null;
var audioContext = new AudioContext();

navigator.webkitGetUserMedia({
  audio: true
}, function (stream) {
  var input = audioContext.createMediaStreamSource(stream);
  recorder = new Recorder(input);
}, function (er) {
  console.log(er);
});
