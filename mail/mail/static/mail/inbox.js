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
  document.querySelector('h3').innerHTML = "New Email";

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault();

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
      load_mailbox('sent'); 
    })
  }

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function compose_reply(subject, recipients){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('h3').innerHTML = "Reply";

  document.querySelector("#compose-recipients").value = recipients;
  document.querySelector('#compose-subject').value = `RE: ${subject}`;

  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault();

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
      load_mailbox('sent'); 
    })
  }
}

function archive_email(archive, emailId){
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archive
    })
  });
  load_mailbox('archived'); 
}

function load_email(email_id, user_email, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = '';

  var id_index = email_id.lastIndexOf("_");
  var id = email_id.substr(id_index + 1);
  // console.log(id)
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    const sender = email.sender;
    const recipients = email.recipients;
    const subject = email.subject;
    const timestamp = email.timestamp;
    const body = email.body;

    let recipient_str = '';
    for (let i = 0; i < recipients.length; i++){
      recipient_str += recipients[i] + " ";
    }

    email_content = `<div class="container">
                      <div class="row">
                        <b>From:</b>
                        <div class="col-auto">${sender}</div>
                      </div>
                      <div class="row">
                        <b>To:</b>
                        <div class="col-auto">${recipient_str}</div>
                      </div>
                      <div class="row">
                        <b>Subject:</b>
                        <div class="col-auto">${subject}</div>
                      </div>
                      <div class="row">
                        <b>Timestamp:</b>
                        <div class="col-auto">${timestamp}</div>
                      </div>
                      <div class="row">
                        <button data-user-email="${user_email}" data-email-id="email_${email_id}" class="btn btn-sm btn-outline-primary" id="reply">Reply</div>
                      </div>
                      <hr>
                      <div class="row d-flex flex-wrap text-left">
                        <div class="col-auto text-left">${body}</div>
                      </div>
                    </div>`
    document.querySelector('#emails-view').insertAdjacentHTML('beforeend', email_content);
    document.querySelector(`#reply`).addEventListener("click", () => compose_reply(subject, sender));

    if (mailbox === "inbox" || mailbox === "archived"){
      console.log(mailbox);
      if (!email.archive){
        console.log('Email is not archived.');
        archive_HTML = `<hr>
                        <div class="row">
                          <button data-user-email="${user_email}" data-email-id="email_${email_id}" class="btn btn-sm btn-outline-primary" id="archive">Unarchive</div>
                        </div>`
        document.querySelector('#emails-view').insertAdjacentHTML('beforeend', archive_HTML);
        document.querySelector(`#archive`).addEventListener("click", () => archive_email(false, email_id));
      } else {
        console.log('Email is archived.');
        unarchive_HTML = `<hr>
                        <div class="row">
                          <button data-user-email="${user_email}" data-email-id="email_${email_id}" class="btn btn-sm btn-outline-primary" id="archive">Archive</div>
                        </div>`
        document.querySelector('#emails-view').insertAdjacentHTML('beforeend', unarchive_HTML);
        document.querySelector(`#archive`).addEventListener("click", () => archive_email(true, email_id));
      }
    }

    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
  });
}

function load_mailbox(mailbox) {  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails.length);
    for (let i = 0; i < emails.length; i++){
      let background_color;
      if (emails[i].read) {
        background_color = "lightgray";
      } else {
        background_color = "white";
      }
      const emailHTML = `<div class="container" style="border: 1px solid;cursor: pointer" id="email_${emails[i].id}">
                            <div class="row justify-content-start" style="background-color: ${background_color}">
                              <div class="col-auto text-left" style="font-weight:bold;">${emails[i].sender}</div>
                              <div class="col-auto text-left">${emails[i].subject}</div>
                              <div class="col text-right" style="font-size: smaller;">${emails[i].timestamp}</div>
                            </div>
                          </div>`;
      document.querySelector('#emails-view').insertAdjacentHTML('beforeend', emailHTML);
      let userEmail;
      const current_button = document.querySelector(`#${mailbox}`);
      if (current_button !== null){
        console.log("Current button is not null");
        userEmail = current_button.getAttribute('data-user-email');
      } else {
        console.log("Current button is null");
        const current_button = document.querySelector(`#archived`);
        userEmail = current_button.getAttribute('data-user-email');
        mailbox = "archived";
      }
      document.querySelector(`#email_${emails[i].id}`).addEventListener("click", () => load_email(`${emails[i].id}`, userEmail, mailbox));
    }
  });
}