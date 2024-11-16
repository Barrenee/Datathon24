document.getElementById('inscriptionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from actually submitting

    // Create the data object
    const data = {
        id: generateUUID(), // Assuming you want to generate a unique id
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        age: parseInt(document.getElementById('age').value),
        year_of_study: document.getElementById('year_of_study').value,
        shirt_size: document.getElementById('shirt_size').value,
        university: document.getElementById('university').value,
        dietary_restrictions: document.getElementById('dietary_restrictions').value,
        interests: getCheckedValues('[id^=interest]'), // Collect checked interests
        preferred_role: document.getElementById('preferred_role').value,
        experience_level: document.getElementById('experience_level').value,
        hackathons_done: parseInt(document.getElementById('hackathons_done').value),
        objective: document.getElementById('objective').value,
        introduction: document.getElementById('introduction').value,
        technical_project: document.getElementById('technical_project').value,
        future_excitement: document.getElementById('future_excitement').value,
        fun_fact: document.getElementById('fun_fact').value,
        preferred_languages: getCheckedValues('[id^=lang]'), // Collect checked languages
        friend_registration: [], // Add friend registration logic if needed
        preferred_team_size: parseInt(document.getElementById('preferred_team_size').value),
        availability: getAvailability(),
        programming_skills: getProgrammingSkills(),
        interest_in_challenges: getCheckedValues('[id^=challenge]') // Collect checked challenges
    };

    console.log(data); // You can send it to your server or handle it as needed

     // Send data to Flask
     fetch('/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Ensure Content-Type is set to application/json
        },
        body: JSON.stringify(data)  // Convert the data object to a JSON string
    })
    .then(response => response.json())
    .then(result => {
        console.log('Form submitted successfully:', result);
    })
    .catch(error => {
        console.error('Error submitting form:', error);
    });
    

    // Helper functions
    function getCheckedValues(selector) {
        return Array.from(document.querySelectorAll(`${selector}:checked`)).map(e => e.value);
    }
    
    function getAvailability() {
        return {
            'Saturday morning': document.getElementById('availability_saturday_morning').checked,
            'Saturday afternoon': document.getElementById('availability_saturday_afternoon').checked,
            'Saturday night': document.getElementById('availability_saturday_night').checked,
            'Sunday morning': document.getElementById('availability_sunday_morning').checked,
            'Sunday afternoon': document.getElementById('availability_sunday_afternoon').checked
        };
    }
    
    function getProgrammingSkills() {
        return {
            'Data Visualization': parseInt(document.getElementById('data_viz').value),
            'Flask': parseInt(document.getElementById('flask').value),
            'React Native': parseInt(document.getElementById('react_native').value),
            'UI/UX Design': parseInt(document.getElementById('ui_ux_design').value),
            'TypeScript': parseInt(document.getElementById('typescript').value),
            'Git': parseInt(document.getElementById('github').value),
            'React': parseInt(document.getElementById('react').value),
            'MongoDB': parseInt(document.getElementById('mongodb').value),
            'HTML/CSS': parseInt(document.getElementById('html').value) + parseInt(document.getElementById('css').value)
        };
    }
  
    function generateUUID() {
        // Helper function to generate a random UUID (simplified)
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
});