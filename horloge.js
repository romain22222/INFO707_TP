const { fork } = require("child_process");
const variable = fork("variable.js");

// init all processus in variable.js

const collectors = [];
for (let i = 0; i < 3; i++) {
  collectors[i] = fork("collector.js");
  //send current pid to variable
  variable.send({ type: "NEW_COLLECTOR", pid: collectors[i] })
}
const controller = fork("controller.js");
variable.send({ type: "NEW_CONTROLLER", pid: controller })


const capteurs = [];
for (let i = 0; i < 3; i++) {
  capteurs[i] = fork("capteur.js");
  //send current pid to variable
  variable.send({ type: "NEW_CAPTEUR", pid: capteurs[i] });
}

// init fini

// Periodically send a signal to the collectors and controller
const delta_1 = 1000; // Replace 1000 with the desired value of delta_1 in milliseconds
setInterval(() => {
    console.log("Sending signal to the collectors and controller")
  for (let i = 0; i < 3; i++) {
    // Send a signal to the collector
    collectors[i].send({ type: "SIGNAL", variable });
  }
  // Send a signal to the controller
  controller.send({ type: "SIGNAL", variable });
}, delta_1);
