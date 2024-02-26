// Dashboard js file

function openSidebar() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("mainContent").style.marginLeft = "250px";
}

function closeSidebar() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("mainContent").style.marginLeft = "0";
}

function logout() {
    // Retrieve the base URL from the data attribute
    var baseUrl = document.body.dataset.baseUrl;
    // Redirect to the logout route using the base URL
    window.location.href = baseUrl + "/signin/admin";
    // Implement logic for logout
    alert('Logged out!');
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

// Profile Models
function openModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

function saveChanges() {
    // Trigger the form submission
    document.getElementById('uploadForm').submit();
    closeModal();
}

function showEditProfileModal() {
    // Logic to populate the form elements in the profile modal with existing user data
    // This can be done using JavaScript DOM manipulation
    const profileModal = document.getElementById('profileModal');
    profileModal.style.display = 'block';
}

function showChangePasswordModal() {
    // Logic to show the change password modal
    // You can implement this based on your requirements
    alert('Change Password Modal');
}

function saveProfileChanges() {
    // Logic to save changes made in the profile modal
    // This could involve making an AJAX request to update user data on the server
    // After saving changes, you can hide the modal
    alert('Profile changes saved!');
    const profileModal = document.getElementById('profileModal');
    profileModal.style.display = 'none';
}

function discardChanges() {
    // Logic to discard changes made in the profile modal
    // This could involve resetting form elements to their initial values
    // After discarding changes, you can hide the modal
    alert('Changes discarded!');
    const profileModal = document.getElementById('profileModal');
    profileModal.style.display = 'none';
}
