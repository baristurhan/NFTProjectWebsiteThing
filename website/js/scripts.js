async function buy(id) {
	console.log("Getting account");
	const account = await getCurrentAccount();
	console.log(`Account is ${account}.\nFetching price...`);
	const price = await getPrice(id);
	const toSend = web3.utils.toWei(price, "ether");
	console.log(`Price is ${price} CETH.\nBegin transaction...`);
	await window.contract.methods.buy(id).send({ from: account, value: toSend });
	console.log("Transaction attempted...");
	
}


async function withdraw() {
	console.log("Getting account");
	const account = await getCurrentAccount();
	console.log(`Account is ${account}.\nFetching balance...`);
	const balance = await getBalance(account);
	console.log(`Balance is ${balance} CETH.\nBegin transaction...`);
	await window.contract.methods.withdraw().send( { from: account } )
	console.log("Transaction attempted...")
}


async function setTokenPrice(id, price) {
	console.log("Getting account");
	const account = await getCurrentAccount();
	console.log(`Account is ${account}.\nBegin transaction...`);
	await window.contract.methods.setTokenPrice().send( { from: account } )
}


async function getBalance(address) {
	return await window.contract.methods.getBalance(address).call();
}

async function getName(id) {
	return await window.contract.methods.getName(id).call();
}

async function getPrice(id) {
	return await window.contract.methods.getPrice(id).call();
}

async function getURI(id) {
	return await window.contract.methods.getURI(id).call();
}

async function getCurrentAccount() {
	const accounts = await window.web3.eth.getAccounts();
	return accounts[0];
}

async function getJSON(path) {
    return fetch(path).then(response => response.json());
}

async function checkNetwork() {
	const networkId = await web3.eth.net.getId();
	if (networkId == 777) {
		return false;
	} else {
		return true;
	}
}

async function loadContract() {
	console.log("Fetching ABI data...");
	
	ABI = await getJSON("./data/ABI.json");
	
	return await new window.web3.eth.Contract(ABI, '0xd9145CCE52D386f254917e481eB44e9943F39138');
}

async function loadWeb3() {
  if (window.ethereum) {
    window.web3 = new Web3(window.ethereum);
    window.contract = await loadContract();
    window.ethereum.eth_requestAccounts;
    console.log("Web3 Loaded...");
  } else {
  	console.log("Failed to load Web3.")
  }
}


async function load() {
  await loadWeb3();
}
load();
