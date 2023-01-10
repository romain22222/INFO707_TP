const { fork } = require("child_process");

process.on("message", (message) => {
  if (message.type === "SIGNAL") {
    console.log("I'm controller Received signal from the clock");
  }
});
