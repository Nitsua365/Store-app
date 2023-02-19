chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  // Get the data from the message
  if (request.status === "done") {
    var messageElement = document.getElementById('loading');
    messageElement.textContent = "Done";
  }
  return true;
});