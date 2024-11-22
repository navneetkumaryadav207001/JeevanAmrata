(function ($) {
    "use strict";

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 40) {
            $('.navbar').addClass('sticky-top');
        } else {
            $('.navbar').removeClass('sticky-top');
        }
    });
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Product carousel
    $(".product-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 45,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
    });
    
})(jQuery);

function toggleChat() {
    var chatWindow = document.getElementById("chatWindow");
    if (chatWindow.style.display === "block") {
        chatWindow.style.display = "none";
    } else {
        chatWindow.style.display = "block";
    }
}

async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (!userInput) return;

    // Display user's message in the chat window
    const chatBody = document.getElementById("chatBody");
    const userMessage = document.createElement("p");
    userMessage.textContent = "You: " + userInput;
    chatBody.appendChild(userMessage);

    // Clear the input field
    document.getElementById("userInput").value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();
        if (data.message) {
            // Display chatbot's response in the chat window
            const botMessage = document.createElement("p");
            botMessage.textContent =data.message;
            botMessage.innerHTML = `Bot: ${marked.parse(data.message)}`;
            chatBody.appendChild(botMessage);
        } else if (data.error) {
            console.error(data.error);
        }

        // Auto-scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = 'Hi';
recognition.interimResults = false;

// Function to start speech recognition
function startRecognition() {
    recognition.start();
    console.log("Voice recognition started. Speak into the microphone...");
}

// Handle recognition result (user's voice converted to text)
recognition.onresult = function(event) {
    const voiceInput = event.results[0][0].transcript;
    document.getElementById('userInput').value = voiceInput;  // Fill the input field with recognized text
    sendMessage(); // Trigger the chatbot's response based on the recognized text
};

// Error handling
recognition.onerror = function(event) {
    console.error("Speech recognition error: ", event.error);
};


function speak(text) {
    const speech = new SpeechSynthesisUtterance();
    speech.text = text; // The text to speak
    speech.lang = 'Hi'; // Set language
    speech.rate = 1; // Speed of speech
    window.speechSynthesis.speak(speech);
}

// Example usage - When chatbot responds
async function sendMessage() {
    const userInput = document.getElementById("userInput").value.trim();
    if (!userInput) return;

    const chatBody = document.getElementById("chatBody");
    const userMessage = document.createElement("p");
    userMessage.textContent = "You: " + userInput;
    chatBody.appendChild(userMessage);

    // Clear input field
    document.getElementById("userInput").value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();
        if (data.message) {
            const botResponse = data.message.trim();
            const botMessage = document.createElement("p");
            botMessage.textContent = "Bot: " + botResponse;
            chatBody.appendChild(botMessage);
            
            // Voice the bot's response
            speak(botResponse);
        } else if (data.error) {
            console.error(data.error);
        }

        // Auto-scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

