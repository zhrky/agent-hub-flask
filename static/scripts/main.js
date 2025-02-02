//Initiate jQuery on load.
let isMuted = false;

$(function() {
  //Translate text with flask route
  var converter = new showdown.Converter();

  $("#send").on("click", function(e) {
    e.preventDefault();
    var oinput = document.getElementById("text-to-send");
    oinput.disabled = true;
    //hide introcards div
    document.getElementById("introcards").style.display = "none";

    var messageVal = oinput.value;
    var translateRequest = { 'text': messageVal }

    var div = document.createElement("div");
    div.textContent = messageVal;
    div.className = "message_user";
    document.getElementById("messages").appendChild(div);
    oinput.value = "";
    document.getElementById("send").disabled = true;
    document.getElementById("send").style.display = "none";
    document.getElementById("micr").style.display = "block";

    if (messageVal !== "") {
      
      $.ajax({
        url: '/generate',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(translateRequest),
        success: function(data) {
            //messages id div içine yeni bir div ekle içinde metin olsun.
            data = JSON.parse(data);
            console.log("data:",data);
            var response = data['choices'][0]['message']['content'];
            var div = document.createElement("div");
            div.innerHTML = converter.makeHtml(response);
            div.className = "message_assistant";
            document.getElementById("messages").appendChild(div);
            var objDiv = document.getElementById("messages");
            //objDiv.scrollTop = objDiv.scrollHeight;
            objDiv.lastElementChild.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
            //document.getElementById("messages").scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"})

            //call tts function
            readTextLoudly(div.textContent);
            oinput.disabled = false;
            document.getElementById("micr").disabled = false;
            oinput.focus();
            document.getElementById("text-to-send").focus();
        },
          error: function(error) {
            console.log("Error: " + error);
            oinput.value = messageVal;
        }
        
      });
    };
    //auto scroll to bottom of messages smoothly
    var objDiv = document.getElementById("messages");
    objDiv.lastElementChild.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})

    
  });

  $("#micr").on("click", function(e) {
    e.preventDefault();
    var oinput = document.getElementById("text-to-send");
    var tempplc = oinput.getAttribute("placeholder");
    oinput.setAttribute("placeholder","Dinliyorum...");
    oinput.disabled = true;
    document.getElementById("micr").disabled = true;
    //hide introcards div
    document.getElementById("introcards").style.display = "none";

    //start listening
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "tr-TR";
    recognition.start();
    recognition.onresult = function(event) {
      var speechResult = event.results[0][0].transcript;
      oinput.value = speechResult;
    };
    recognition.onend = function() {
      document.getElementById("send").disabled = false;
      document.getElementById("micr").disabled = false;
      document.getElementById("send").click();
      oinput.setAttribute("placeholder",tempplc);
      recognition.stop();
    };

  });

  $(".ccard").on("click", function(e) {
      ccard = e.target;
      var oinput = document.getElementById("text-to-send");
      oinput.value = ccard.innerHTML;
      document.getElementById("send").disabled = false;
      document.getElementById("send").style.display = "block";
      document.getElementById("micr").style.display = "none";
  });

  function readTextLoudly(text) {

    let inputText = text.replace(/https?:\/\/[^\s]+/g, '').replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, '');
    
    if(!isMuted){
      //unmute synthesizer
      synthesizer.speakTextAsync(
        inputText,
        function (result) {
          console.log("reading:"+inputText);
          // window.console.log(result);
          // synthesizer.close();
          // synthesizer = undefined;
        },
        function (err) {
          window.console.log(err);
          // synthesizer.close();
          // synthesizer = undefined;
    });
    }
  }

//focus on input on load
  document.getElementById("text-to-send").focus();

});



document.addEventListener("DOMContentLoaded", function() {

  // Get the input field and send button
  var inputField = document.getElementById("text-to-send");
  var sendButton = document.getElementById("send");
  var micrButton = document.getElementById("micr");
  sendButton.disabled = true

  text = document.getElementById("messages").firstElementChild.textContent;
  

  // Add event listener to input field
  inputField.addEventListener("input", function() {
      if (inputField.value.length > 0) {
          sendButton.disabled = false;
          micrButton.disabled = true;
          sendButton.style.display = "block";
          micrButton.style.display = "none";
      } else {
          sendButton.disabled = true;
          micrButton.disabled = false;
          sendButton.style.display = "none";
          micrButton.style.display = "block";
      }
  });

  const volumeControl = document.getElementById('volume-control');
  const volumeIcon = document.getElementById('volume-icon');

  volumeIcon.addEventListener('click', function() {
      isMuted = !isMuted;
      if (isMuted) {
          volumeIcon.classList.remove('fa-volume-up');
          volumeIcon.classList.add('fa-volume-mute');
          player.mute();
          // Example: document.getElementById('audio-element').muted = true;
      } else {
          volumeIcon.classList.remove('fa-volume-mute');
          volumeIcon.classList.add('fa-volume-up');
          player.unmute();
          // Example: document.getElementById('audio-element').muted = false;
      }
  });

});

