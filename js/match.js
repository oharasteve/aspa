// Match scoring dumb app

// TODO: back end for getting match
// TODO: back end hit for match results
// TODO: invalid break foul

// Stolen from https://www.wintellect.com/data-binding-pure-javascript/

function Binding(b) {
  var _this = this
  this.element = b.element
  this.value = b.object[b.property]
  this.attribute = b.attribute
  this.valueGetter = function() {
    return _this.value;
  }
  this.valueSetter = function(val) {
    _this.value = val
    _this.element[_this.attribute] = val
  }

  Object.defineProperty(b.object, b.property, {
    get: this.valueGetter,
    set: this.valueSetter
  });
  b.object[b.property] = this.value;
  this.element[this.attribute] = this.value
}

// Parse out GET parameters
function getSearchParameters() {
    var prmstr = window.location.search.substr(1);
    return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
}

function transformToAssocArray( prmstr ) {
    var params = {};
    var prmarr = prmstr.split("&");
    for ( var i = 0; i < prmarr.length; i++) {
        var tmparr = prmarr[i].split("=");
        params[tmparr[0]] = tmparr[1];
    }
    return params;
}

var params = getSearchParameters();

// Core logic
var p1 = {
  name: params.p1_name,
  target: params.p1_target,
  score: 0,
  this_rack: 0,
  high_run: 0,
  fouls: 0,
  progress: document.getElementById("p1_progress_outer")
};
var p2 = {
  name: params.p2_name,
  target: params.p2_target,
  score: 0,
  this_rack: 0,
  high_run: 0,
  fouls: 0,
  progress: document.getElementById("p2_progress_outer")
};

var game = {
  run: 0,
  rack_run: 0,
  rack: 15,
  current_player: p1
};

document.getElementById("p1_name").innerText = params.p1_name;
document.getElementById("p2_name").innerText = params.p2_name;
document.getElementById("p1_target").innerText = params.p1_target;
document.getElementById("p2_target").innerText = params.p2_target;
document.title = p1.name + " vs " + p2.name;

p1.progress.style.backgroundImage = "repeating-linear-gradient(to right, transparent, black 0 1px, transparent 1px " + (100 / p1.target) + "%)";
p2.progress.style.backgroundImage = "repeating-linear-gradient(to right, transparent, black 0 1px, transparent 1px " + (100 / p2.target) + "%)";

// Player 1
var bind_p1_score = new Binding({
  object: p1,
  property: "score",
  element: document.getElementById("p1_score"),
  attribute: "innerText"
});
var bind_p1_rack = new Binding({
  object: p1,
  property: "this_rack",
  element: document.getElementById("p1_this_rack"),
  attribute: "innerText"
});
var bind_p1_hr = new Binding({
  object: p1,
  property: "high_run",
  element: document.getElementById("p1_high_run"),
  attribute: "innerText"
});
var bind_p1_fouls = new Binding({
  object: p1,
  property: "fouls",
  element: document.getElementById("p1_fouls"),
  attribute: "innerText"
});
// Player 2
var bind_p2_score = new Binding({
  object: p2,
  property: "score",
  element: document.getElementById("p2_score"),
  attribute: "innerText"
});
var bind_p2_rack = new Binding({
  object: p2,
  property: "this_rack",
  element: document.getElementById("p2_this_rack"),
  attribute: "innerText"
});
var bind_p2_hr = new Binding({
  object: p2,
  property: "high_run",
  element: document.getElementById("p2_high_run"),
  attribute: "innerText"
});
var bind_p2_fouls = new Binding({
  object: p2,
  property: "fouls",
  element: document.getElementById("p2_fouls"),
  attribute: "innerText"
});
// Other stats
var bind_game_run = new Binding({
  object: game,
  property: "run",
  element: document.getElementById("run"),
  attribute: "innerText"
});
var bind_game_rack_run = new Binding({
  object: game,
  property: "rack_run",
  element: document.getElementById("rack_run"),
  attribute: "innerText"
});
var bind_game_rack = new Binding({
  object: game,
  property: "rack",
  element: document.getElementById("rack"),
  attribute: "innerText"
});

function end_of_inning() {
  game.current_player.score += game.rack_run;
  var points = game.run;
  if (points > game.current_player.score) {
      points = game.current_player.score;
  }
  if (points > 0) {
    game.current_player.progress.lastElementChild.style.width = "" + ((points / game.current_player.target) * 100) + "%";
    var progress = document.createElement('span');
    progress.classList.add("progress");
    game.current_player.progress.appendChild(progress);
  }
  game.current_player.this_rack += game.rack_run;
  if (game.current_player.high_run < game.run) {
    game.current_player.high_run = game.run;
  }
  if (game.current_player.score >= game.current_player.target) {
    alert(game.current_player.name + " Wins");
  }
  game.rack_run = 0;
  game.run = 0;
  if (game.current_player == p1) {
    game.current_player = p2;
  } else {
    game.current_player = p1;
  }
  document.getElementById("player1").classList.toggle("active");
  document.getElementById("player2").classList.toggle("active");
}

function end_of_rack() {
  var p1_score = p1.this_rack;
  var p2_score = p2.this_rack;
  if (game.current_player == p1) {
    p1_score += game.rack_run;
    p1.score += game.rack_run;
  } else {
    p2_score += game.rack_run;
    p2.score += game.rack_run;
  }
  var points = game.run;
  if (points > game.current_player.score) {
      points = game.current_player.score;
  }
  game.current_player.progress.lastElementChild.style.width = "" + ((points / game.current_player.target) * 100) + "%";
  alert("End of rack " + p1_score + " to " + p2_score);
  p1.this_rack = 0;
  p2.this_rack = 0;
  game.rack_run = 0;
  game.rack = 15;
}

function plus1() {
  game.run += 1;
  game.rack_run += 1;
  game.rack -= 1;
  if (game.rack <= 1) {
    end_of_rack();
  }
}

function plus5() {
  if (game.rack <= 5) {
      retrun;
  }
  game.run += 5;
  game.rack_run += 5;
  game.rack -= 5;
  if (game.rack <= 1) {
    end_of_rack();
  }
}

function plus14() {
  // Run out the remainder of the rack.
  game.run += game.rack-1;
  game.rack_run = game.rack-1;
  game.rack = 1;
  end_of_rack();
}

function minus1() {
  game.run -= 1;
  game.rack_run -= 1;
  game.rack += 1;
}

function miss() {
  game.current_player.fouls = 0;
  end_of_inning();
}

function remove_point() {
  var previous = game.current_player.progress.lastElementChild.previousElementSibling;
  if (previous == null) {
    return;
  }
  var last_run = +previous.style.width.slice(0,-1);
  var new_width = (last_run - ((1 / game.current_player.target) * 100));
  if (new_width <= 0.05) { // Rounding error for 0
    previous.remove();
  } else {
    previous.style.width = "" + new_width + "%";
  }
}

function foul() {
  if (game.run != 0) {
    game.current_player.fouls = 0;
  }

  remove_point();
  game.current_player.fouls += 1;
  game.current_player.score -= 1;
  if (game.current_player.fouls == 3) {
    game.current_player.score -= 15;
    for(i = 0; i < 15; i++) { remove_point(); }
    game.current_player.fouls = 0;
    alert(game.current_player.name + " 3 foul'd");
    end_of_rack();
    return;
  }
  end_of_inning();
}

