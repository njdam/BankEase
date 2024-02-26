// Dashboard js file
// var sidebarOpen = false;
function toggleSidebar() {
	if (sidebarOpen) {
		closeSidebar();
	} else {
		openSidebar();
	}
}
/*
function openSidebar() {
	// Your code to open the sidebar
	console.log('Sidebar opened');
	sidebarOpen = true;
}

function closeSidebar() {
	// Your code to close the sidebar
	console.log('Sidebar closed');
	sidebarOpen = false;
}
*/
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
    // Redirect to the logout route using Flask's url_for function
    window.location.href = '{{ url_for("logout") }}';
    // Implement logic for logout
    alert('Logged out!');
}

function switchAccount(accountName) {
    // Implement logic to switch account
    alert('Switched to ' + accountName);
    // Update account details in the main content section
    document.querySelector('.account-info span').textContent = 'Account Number: ' + accountName + 'XXXX';
    // Fetch and update account information (replace with actual data fetching logic)
    document.querySelector('.account-info p:first-child').textContent = 'Account Number: ' + accountName + 'XXXX';
}

// Predefined list of country codes and names
const countryCodes = [
    { code: '+250', name: 'Rwanda'},
    { code: '+1', name: 'United States' },
    { code: '+44', name: 'United Kingdom' },
    // Add more countries as needed
];

// Function to populate the country code dropdown
function populateCountryCodes() {
    const countryCodeDropdown = document.getElementById('countryCode');

    // Loop through the country codes and add options to the dropdown
    countryCodes.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.text = `${country.code} (${country.name})`;
        countryCodeDropdown.add(option);
    });
    // Set the initial value based on the passed user phone number
    const initialPhoneNumber = '{{ User.phone_number }}'; // Example value

    // Set the initial value for the phone number input
    document.getElementById('editPhoneNumber').value = initialPhoneNumber;
}

// Call the function to populate the dropdown when the page loads
document.addEventListener('DOMContentLoaded', populateCountryCodes);
