const { fork } = require("child_process");

const collectors = [];
for (let i = 0; i < 3; i++) {
  collectors[i] = fork("collector.js");
}
const controller = fork("controller.js");

// Periodically send a signal to the collectors and controller
const delta_1 = 1000; // Replace 1000 with the desired value of delta_1 in milliseconds
setInterval(() => {
    console.log("Sending signal to the collectors and controller")
  for (let i = 0; i < 3; i++) {
    // Send a signal to the collector
    collectors[i].send({ type: "SIGNAL" });
  }
  // Send a signal to the controller
  controller.send({ type: "SIGNAL" });
}, delta_1);
