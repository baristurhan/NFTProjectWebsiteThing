
/*
async function printCoolNumber() {
	updateStatus('Fetching the cool number...');
	const chainId = await web3.eth.net.getId();
	const coolNumber = await window.contract.methods.GetCoolNumber().call();
	updateStatus(`The cool number is: ${coolNumber}`);
}
*/

/*
async function changeCoolNumber() {
	const value = Math.floor(Math.random()*100);
	updateStatus(`Updating the cool number as ${value}`);
	const account = await getCurrentAccount();
	const coolNumber = await window.contract.methods.SetCoolNumber(value).send({ from: account });
	updateStatus('Updated...');
}
*/

async function getCurrentAccount() {
	const accounts = await window.web3.eth.getAccounts();
	return accounts[0];
}

function getJSON(path) {
    return fetch(path).then(response => response.json());
}

async function loadContract() {
	console.log("Fetching ABI data...");
	
	ABI = getJSON("./data/ABI.json");
	
	console.log(ABI);
	
	return await new window.web3.eth.Contract(ABI, '0xd9145CCE52D386f254917e481eB44e9943F39138');
}

async function loadWeb3() {
  if (window.ethereum) {
    window.web3 = new Web3(window.ethereum);
    window.contract = await loadContract();
    window.ethereum.enable();
    console.log("Web3 Loaded...");
  } else {
  	console.log("Failed to load Web3.")
  }
}

async function load() {
  await loadWeb3();
}
load();
