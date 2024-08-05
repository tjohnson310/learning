document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-form').onsubmit = function() {
    const email_recipients = document.querySelector("#compose-recipients").value;
    const email_subject = document.querySelector("#compose-subject").value;
    const email_body = document.querySelector("#compose-body").value;

    fetch('/emails', {
      method: "POST",
      body: JSON.stringify({
        recipients: email_recipients,
        subject: email_subject,
        body: email_body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });
  }

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  const button = document.querySelector(`#${mailbox}`);
  const userEmail = button.getAttribute('data-user-email');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    for (let i = 0; i < emails.length; i++){
      document.querySelector('#emails-view').innerHTML += `<div class="row container align-items-center" style="border: 1px solid">
                                                          <div class="col"">${emails[i].sender}: </div>
                                                          <div class="col text-left" style="font-weight:bold; font-size: large;">${emails[i].subject}</div>
                                                          </div>`;
    }
  });
}