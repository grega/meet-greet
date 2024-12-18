let previousParticipants = 0;

function checkParticipants() {
    const participantList = document.querySelector('div[role="list"][aria-label="Participants"]');

    if (!participantList) {
        console.warn("Participant list not found.");
        return;
    }

    // select only children of the participant list
    const participantElements = participantList.querySelectorAll('[role="listitem"], [data-participant-id]');

    // extract unique participant identifiers (fallback to innerText)
    const participantIds = new Set([...participantElements].map(el => el.getAttribute('data-participant-id') || el.innerText || ''));

    const participantCount = participantIds.size;

    console.log(`Current number of participants: ${participantCount}`);

    if (participantCount > previousParticipants) {
        console.log('New participant joined');
        fetch('http://localhost:5000/participant-joined')
            .then(() => console.log('Participant joined event sent to server'))
            .catch(err => console.error('Error notifying server:', err));
    }

    previousParticipants = participantCount;
}

setInterval(checkParticipants, 1000);
