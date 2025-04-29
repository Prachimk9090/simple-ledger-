import streamlit as st
import hashlib
import time
import json

# -------------------------------
# Blockchain classes
# -------------------------------

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # e.g., {"description": "Coffee", "amount": -3.5}
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_data = {"description": "Genesis Block", "amount": 0}
        genesis_block = Block(0, time.time(), genesis_data, "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current, previous = self.chain[i], self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="Blockchain Ledger", layout="centered")
st.title("📒 Simple Blockchain Ledger")

# Use session state to persist the blockchain across interactions
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Add a transaction
with st.form("transaction_form"):
    st.subheader("➕ Add Transaction")
    description = st.text_input("Description")
    amount = st.number_input("Amount", step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if description.strip() == "":
            st.warning("Description cannot be empty.")
        else:
            st.session_state.blockchain.add_block({"description": description, "amount": amount})
            st.success("Transaction added to the blockchain.")

# Display the blockchain
st.subheader("🔗 Blockchain Ledger")
for block in st.session_state.blockchain.chain:
    with st.expander(f"Block {block.index}"):
        st.write(f"**Timestamp:** {time.ctime(block.timestamp)}")
        st.write(f"**Data:** {block.data}")
        st.write(f"**Hash:** `{block.hash}`")
        st.write(f"**Previous Hash:** `{block.previous_hash}`")

# Validate the blockchain
st.subheader("✅ Blockchain Validation")
if st.session_state.blockchain.is_chain_valid():
    st.success("The blockchain is valid.")
else:
    st.error("The blockchain is invalid!")
