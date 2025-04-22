async function queryData() {
    const questionInput = document.getElementById("question");
    const question = questionInput.value;
    const chatMessages = document.getElementById("chat-messages");

    // Add user message to chat
    const userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("message", "user-message");
    userMessageDiv.textContent = question;
    chatMessages.appendChild(userMessageDiv);

    questionInput.value = ""; // Clear the input
    const loader = document.getElementById("loader");
    loader.style.display = "block";
    const requestTimeDiv = document.getElementById("request-time");
    let startTime = new Date().getTime();
    let intervalId = setInterval(() => {
        let elapsedTime = new Date().getTime() - startTime;
        requestTimeDiv.textContent = `Request time: ${(elapsedTime / 1000).toFixed(2)} seconds`;
        requestTimeDiv.style.display = "block";
    }, 100);

    const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: question })
    });

    const data = await response.json();
    loader.style.display = "none";
    clearInterval(intervalId);
    // const requestTimeDiv = document.getElementById("request-time");
    // requestTimeDiv.textContent = `Request time: ${data.request_time.toFixed(2)} seconds`;
    // requestTimeDiv.style.display = "block";

    // data.results.forEach(result => {
    const botMessageDiv = document.createElement("div");
    botMessageDiv.classList.add("message", "bot-message");
    botMessageDiv.textContent = data.answer;
    chatMessages.appendChild(botMessageDiv);
    // });

    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
}