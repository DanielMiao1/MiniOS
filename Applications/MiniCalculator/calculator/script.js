function addChar(char) {
  if (document.getElementById("text").value == "" && [" ÷ ", " + ", " × "].includes(char)) {
    return
  }
  if ([" ÷ ", " + ", " × "].includes(char)) {
    if (document.getElementById("text").value == "") {
      document.getElementById("text").value = document.getElementById("text").value + char
    }
    else if (document.getElementById("text").value.slice(document.getElementById("text").value.length - 1, document.getElementById("text").value.length) == " ") {
      return
    }
  }
  if (char == " – " && document.getElementById("text").value == "") {
    document.getElementById("text").value = " – "
  }
  else if (char == ".") {
    if ((equationToArray()[equationToArray().length - 1]).includes(".")) {
      return
    }
    document.getElementById("text").value = document.getElementById("text").value + char
  }
  else {
    document.getElementById("text").value = document.getElementById("text").value + char
  }
}
function calculate() {
  if (document.getElementById("text").value != "") {
    document.getElementById("text").value = eval("(" + (evaluateEquation()).toString() + ") * 1")
  }
}
function evaluateEquation() {
  var new_equation = ""
  for (var x of (document.getElementById("text").value).split("")) {
    if (x.toString() == "×") {
      new_equation += "*"
    }
    else if (x.toString() == "–") {
      new_equation += "-"
    }
    else if (x.toString() == "÷") {
      new_equation += "/"
    }
    else {
      new_equation += x.toString()
    }
  }
  return new_equation
}
function switchOperators() {
  if ((document.getElementById("text").value).toString().includes(" ")) {
    return
  }
  else if ((document.getElementById("text").value).toString() == "") {
    return
  }
  if ((document.getElementById("text").value).toString().startsWith("-")) {
    document.getElementById("text").value = document.getElementById("text").value.slice(1, document.getElementById("text").value.length)
  }
  else {
    document.getElementById("text").value = "-" + document.getElementById("text").value
  }
}
function key(event) {
  if (event.key == "Enter") {
    document.getElementById("=").click()
  }
  else if (["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Backspace", "c", "+", "-", "*", "/", "=", "."].includes(event.key)) {
    document.getElementById((event.key).toString()).click()
  }
}
function clearEntry() {
  if (document.getElementById("text").value == "") {
    return
  }
  if (["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "-"].includes(document.getElementById("text").value.slice(document.getElementById("text").value.length - 1, document.getElementById("text").value.length))) {
    document.getElementById("text").value = document.getElementById("text").value.slice(0, document.getElementById("text").value.length - 1)
  }
  else if (document.getElementById("text").value.slice(document.getElementById("text").value.length - 1, document.getElementById("text").value.length) == " ") {
    document.getElementById("text").value = document.getElementById("text").value.slice(0, document.getElementById("text").value.length - 3)
  }
}
function equationToArray() {
  var equation = document.getElementById("text").value
  var new_equation = ""
  for (var x of equation.split("")) {
    if (x.toString() == "×") {
      new_equation += "*"
    }
    else if (x.toString() == "–") {
      new_equation += "-"
    }
    else if (x.toString() == "÷") {
      new_equation += "/"
    }
    else {
      new_equation += x.toString()
    }
  }
  var numbers = new_equation.split(/[+,-,*,/]+/)
  for (x of numbers) {
    if (x.startsWith(" ")) {
      numbers[numbers.indexOf(x)] = x.slice(1, x.length)
    }
    if (x.endsWith(" ")) {
      numbers[numbers.indexOf(x)] = x.slice(0, x.length - 1)
    }
  }
  return numbers
}
