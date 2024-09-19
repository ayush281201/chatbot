var dict = {'dealer_id':390}
localStorage.setItem('currentSetting', JSON.stringify(dict))
var dealerID = JSON.parse(localStorage.getItem('currentSetting'))
var dealer_id=String(dealerID['dealer_id'])
$(document).ready(function() {
    const filePath = 'train/training'+ dealer_id +'.jsonl';
    $.ajax({
        url: '/delete-file',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ filePath: filePath }),
        success: function(response) {
            console.log('File deleted successfully:', response);
        },
        error: function(xhr) {
            console.error('Error deleting file:', xhr.responseJSON.message);
        }
    });
    const filePath1 = 'dealer'+ dealer_id + '.jsonl';
    $.ajax({
        url: '/delete-file',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ filePath: filePath1 }),
        success: function(response) {
            console.log('File deleted successfully:', response);
        },
        error: function(xhr) {
            console.error('Error deleting file:', xhr.responseJSON.message);
        }
    });
});
function hideBotTyping() {
    $("#botAvatar").remove();
    $(".botTyping").remove();
}

function showBotTyping() {
    const botTyping = '<img class="botAvatar" id="botAvatar" src="/static/img/botAvatar.jpg"/><div class="botTyping"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div>';
    $(botTyping).appendTo("#chat-body");
    $(".botTyping").show();
}


$('.message_bot').hide();
$('.botAvatar').hide();
function displaybox(){
    const chatbox = document.getElementById('chatbox');
    if(getComputedStyle(chatbox).display == 'block'){
        // $("#chatbox").fadeOut(1000)
        chatbox.style.animation = "zoomOutDown 1s";
        $(".message_user").hide();
        $(".message_bot").hide();
        $(".userAvatar").hide();
        $(".botAvatar").hide();
        setTimeout(()=>{
            chatbox.style.display = "none";
        }, 950)
    } else {
        // $("#chatbox").fadeIn(1000);
        chatbox.style.display = "block"
        chatbox.style.animation = "zoomInUp 1s";
        setTimeout(()=>{
            $(".message_user").show();
            $(".message_bot").show();
            $(".userAvatar").show();
            $(".botAvatar").show();
        }, 950)
    }
}

document.addEventListener('DOMContentLoaded', ()=>{
    async function sendMessage() {
        const userMessage = document.getElementById('user-message').value;
        if(!userMessage.trim()) return;
        const chatBody = document.getElementById('chat-body');
        const userImage = document.createElement('img');
        userImage.setAttribute("src", "/static/img/userAvatar.jpg");
        userImage.setAttribute("class", "userAvatar");
        const userMessageDiv = document.createElement('p');
        const gapDiv = document.createElement('div');
        userMessageDiv.className = "message_user";
        userMessageDiv.textContent = userMessage;
        gapDiv.className = "clearfix";
        chatBody.appendChild(userImage);
        chatBody.appendChild(userMessageDiv);
        chatBody.appendChild(gapDiv);
        document.getElementById("user-message").value = "";
        showBotTyping();
        chatBody.scrollTop = chatBody.scrollHeight;
        try {
            const response = await fetch("/chat", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'dealerId': dealer_id,
                    'message': userMessage
                })
            });
            const data = await response.json();
            const botResponse = data.response;
            const gapDiv = document.createElement('div');
            setTimeout(()=>{
                hideBotTyping()
                if (botResponse.length < 1) {
                    const fallbackMsg = "I am facing some issues, please try again later!!!";              
                    const BotResponse = `<img class='botAvatar' src='./static/img/botAvatar.png'/><p class='message_bot'>${fallbackMsg}</p><div class='clearfix'></div>`;
                
                    $(BotResponse).appendTo("#chat-body").hide().fadeIn(1000);
                }
                const botMessageDiv = document.createElement('p');
                const botImage = document.createElement('img');
                botImage.setAttribute("src", "/static/img/botAvatar.jpg");
                botImage.setAttribute("class", "botAvatar");
                botMessageDiv.className = 'message_bot';
                botMessageDiv.textContent = botResponse;
                gapDiv.className = "clearfix";
                chatBody.appendChild(botImage);
                chatBody.appendChild(botMessageDiv);
                chatBody.appendChild(gapDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            }, 500)
        } catch(error) {
            console.error('Error sending message:', error);
        }
    }
    document.getElementById('user-message').addEventListener('keydown', (event)=>{
        if(event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});

async function sendMessage() {
    const userMessage = document.getElementById('user-message').value;
    if (!userMessage.trim()) return;
    const chatBody = document.getElementById('chat-body');
    const userImage = document.createElement('img');
    userImage.setAttribute("src", "/static/img/userAvatar.jpg");
    userImage.setAttribute("class", "userAvatar");
    const userMessageDiv = document.createElement('p');
    const gapDiv = document.createElement('div');
    gapDiv.className = 'clearfix';
    userMessageDiv.className = 'message_user';
    userMessageDiv.textContent = userMessage;
    chatBody.appendChild(userImage);
    chatBody.appendChild(userMessageDiv);
    chatBody.appendChild(gapDiv);
    document.getElementById('user-message').value = '';
    showBotTyping();
    chatBody.scrollTop = chatBody.scrollHeight;
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'dealerId': dealer_id,
                'message': userMessage
            })
        });
        const data = await response.json();
        const botResponse = data.response;
        const botMessageDiv = document.createElement('p');
        const gapDiv = document.createElement('div');
        const botImage = document.createElement('img');
        botImage.setAttribute("src", "/static/img/botAvatar.jpg");
        botImage.setAttribute("class", "botAvatar");
        botMessageDiv.className = 'message_bot';
        botMessageDiv.textContent = botResponse;
        gapDiv.className = "clearfix";
        chatBody.appendChild(botImage);
        chatBody.appendChild(botMessageDiv);
        chatBody.appendChild(gapDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    } catch (error) {
        console.error('Error sending message:', error);
    }
}