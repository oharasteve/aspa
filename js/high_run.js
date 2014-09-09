function getHighRunTarget(handicap) {
  if (handicap < 100 || handicap >= 850) {
    return 0;
  }

  // This is a lookup table for calculating high run target,
  // given a player's handicap. It is a piecewise linear function,
  // interpolating between the points
  highRuns = [
    [400, 18],
    [450, 20],
    [500, 22],
    [550, 26],
    [600, 32],
    [650, 44],
    [700, 58],
    [725, 72],
    [750, 86],
    [775, 100],
    [800, 114],
    [825, 128],
    [850, 144]
  ];

  for (var i = 0; i < highRuns.length; i++) {
    if (handicap < highRuns[i][0]) {
      break;
    }
  }
  var prev_handicap = 0;
  var prev_target = 0;
  if (i > 0) {
    prev_handicap = highRuns[i-1][0];
    prev_target = highRuns[i-1][1];
  }
  var scale = (highRuns[i][0] - prev_handicap) / (highRuns[i][1] - prev_target);
  return Math.round(prev_target + (handicap - prev_handicap) / scale);
}

function setHighRunTarget(handicapName, highRunTargetName) {
  var handicapElement = document.getElementById(handicapName);
  var highRunElement = document.getElementById(highRunTargetName);
  target = getHighRunTarget(handicapElement.value);
  if (target > 0) {
    highRunElement.value = target;
  } else {
    highRunElement.value = "";
  }
}
