// Transfer Features
function fetchRecipientDetails() {
	var recipientAccount = $('#account_number').val();

        // Make AJAX request to fetch recipient details
        $.ajax({
            url: '{{ url_for("get_recipient_details") }}',
            method: 'POST',
            data: { account_number: recipientAccount },
            success: function(response) {
                console.log('Received response:', response);
                // Update the recipientDetailsBox div with the received data
                if (response.full_name) {
                    $('#recipientDetailsBox').html('<div class="recipient-details">' + response.full_name + '</div>');
                } else {
                    $('#recipientDetailsBox').html('<div class="recipient-details-error">' + response.error + '</div>');
                }
            },
            error: function(error) {
                console.error('Error fetching recipient details:', error);
            }
        });
    }

/*function toggleSidebar() {
	if (sidebarOpen) {
		closeSidebar();
	} else {
		openSidebar();
	}
}

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
