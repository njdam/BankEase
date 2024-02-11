// Dashboard js file
function openSidebar() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("mainContent").style.marginLeft = "250px";
}

function closeSidebar() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("mainContent").style.marginLeft = "0";
}

function openProfileModal() {
    document.getElementById("profileModal").style.display = "block";
}

function saveProfileChanges() {
    // Implement logic to save profile changes
    alert('Profile changes saved!');
    document.getElementById("profileModal").style.display = "none";
}

function discardChanges() {
    // Implement logic to discard changes
    alert('Changes discarded!');
    document.getElementById("profileModal").style.display = "none";
}

function openProfilePage() {
    window.location.href = '{{ url_for("profile") }}';
}

function logout() {
    // Implement logic for logout
    alert('Logged out!');
    // Redirect to the login page or any other desired action
    window.location.href = '{{ url_for("logout") }}';
}

function switchAccount(accountName) {
    // Implement logic to switch account
    alert('Switched to ' + accountName);
    // Update account details in the main content section
    document.querySelector('.account-info span').textContent = 'Account Number: ' + accountName + 'XXXX';
    // Fetch and update account information (replace with actual data fetching logic)
    document.querySelector('.account-info p:first-child').textContent = 'Account Number: ' + accountName + 'XXXX';
}