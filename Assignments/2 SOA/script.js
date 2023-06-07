async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const url = "http://localhost:8000/auth/login/";
  
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.token);
      // redirect to dashboard or homepage
    } else {
      const error = await response.json();
      alert(error.detail);
    }
  }

  async function createUser() {
    const username = document.getElementById("new_username").value;
    const password = document.getElementById("new_password").value;
    const role = document.getElementById("new_role").value;
    const token = localStorage.getItem("token");    
    const url = "http://localhost:8000/auth/manage/?token=" + token + "";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        role,}
      ),

    });
  
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
  
    return response.status;
  }

  async function changeRole() {
    const username = document.getElementById("change_username").value;
    const role = document.getElementById("change_role").value;
    const token = localStorage.getItem("token");    
    const url = "http://localhost:8000/auth/manage/?token=" + token + "";
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        role,}
      ),

    });
  
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
  
    return response.status;
  }

  async function deleteUser() {
    const username = document.getElementById("delete_username").value;
    const token = localStorage.getItem("token");    
    const url = "http://localhost:8000/auth/manage/?token=" + token + "&username=" + username + "";
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },

    });
  
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
  
    return response.status;
  }

  async function createJob() {
    const date_range = document.getElementById("date-range").value;
    const a = document.getElementById("assets").value;
    // convert assets to array
    const assets = a.split(",");
    // convert each element to int
    for (let i = 0; i < assets.length; i++) {
      assets[i] = parseInt(assets[i]);
    } 
    const token = localStorage.getItem("token");
    const url = "http://localhost:8001/master/job/?token=" + token + "";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        date_range,
        assets,
      }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
    return response.status;
  }


  async function createResult() {
    const job_id = document.getElementById("job-id").value;
    const  a = document.getElementById("result_assets").value;
    const assets = a.split(",");
    for (let i = 0; i < assets.length; i++) {
      assets[i] = parseInt(assets[i]);
    }
    const token = localStorage.getItem("token");
    const url = "http://localhost:8001/master/result/?token=" + token + "";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_id,
        assets,}
      ),
        
    });
    if (!response.ok) {
      const error = await response.json();
      alert(error.detail);
    }
    return response.status;
  }

  async function updateJob() {
    const job_id = document.getElementById("job-id-update").value;
    const token = localStorage.getItem("token");
    const url = "http://localhost:8001/master/job/" + job_id + "/?token=" + token + "";
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      const error = await response.json();
      alert(error.detail);
    }
    return response.status; 
  }


  async function getJobs() {
    const token = localStorage.getItem("token");
    const url = "http://localhost:8001/master/jobs/?token=" + token + "";
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      const error = await response.json();
      alert(error.detail);
    }
    const data = await response.json();
    let jobsTable = '<table border>';
    jobsTable += '<tr><th>ID</th><th>User</th><th>Timestamp</th><th>Status</th><th>Date Range</th><th>Assets</th></tr>';
    for (let i = 0; i < data.length; i++) {
      jobsTable += '<tr>';
      jobsTable += '<td>' + data[i].id + '</td>';
      jobsTable += '<td>' + data[i].user + '</td>';
      jobsTable += '<td>' + data[i].timestamp + '</td>';
      jobsTable += '<td>' + data[i].status + '</td>';
      jobsTable += '<td>' + data[i].date_range + '</td>';
      jobsTable += '<td>' + data[i].assets + '</td>';
      jobsTable += '</tr>';
    }
    jobsTable += '</table>';
    document.getElementById('jobs').innerHTML = jobsTable;
    // this will generate a table in div with id="jobs", job has id, user, timestamp, status, date_range, assets
    
    
    
  }
  async function getResults() {
    const token = localStorage.getItem("token");
    const url = "http://localhost:8001/master/results/?token=" + token + "";
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      const error = await response.json();
      alert(error.detail);
    }
    const data = await response.json();
    let resultsTable = '<table border>';
    resultsTable += '<tr><th>ID</th><th>Job ID</th><th>Timestamp</th><th>Assets</th></tr>';
    for (let i = 0; i < data.length; i++) {
      resultsTable += '<tr>';
      resultsTable += '<td>' + data[i].id + '</td>';
      resultsTable += '<td>' + data[i].job_id + '</td>';
      resultsTable += '<td>' + data[i].timestamp + '</td>';
      resultsTable += '<td>' + data[i].assets + '</td>';
      resultsTable += '</tr>';
    }
    resultsTable += '</table>';
    document.getElementById('results').innerHTML = resultsTable;
    // this will generate a table in div with id="results", result has id, job_id, timestamp, assets
  }