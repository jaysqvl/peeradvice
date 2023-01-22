
var signInBtnStudent = document.getElementById("signInBtnStudent");
var signInBtnAdvisor = document.getElementById("signInBtnAdvisor");

// Add a click event listener to the first button
signInBtnStudent.addEventListener("click", function () {
    // Sign in with Google
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider).then(function (result) {
        // User is authenticated, redirect to page 1
        window.location.href = "student.html";
    }).catch(function (error) {
        // Handle errors
        console.error(error);
    });
});

// Add a click event listener to the second button
signInBtnAdvisor.addEventListener("click", function () {
    // Sign in with Google
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider).then(function (result) {
        // User is authenticated, redirect to page 2
        window.location.href = "advisor.html";
    }).catch(function (error) {
        // Handle errors
        console.error(error);
    });
});



// ///// User Authentication /////

// ///// User Authentication /////

// const auth = firebase.auth();

// const whenSignedIn = document.getElementById('whenSignedIn');
// const whenSignedOut = document.getElementById('whenSignedOut');

// const signInBtnStudent = document.getElementById('signInBtnStudent');
// const signInBtnAdvisor = document.getElementById('signInBtnAdvisor');

// const signOutBtn = document.getElementById('signOutBtn');

// const userDetails = document.getElementById('userDetails');


// const provider = new firebase.auth.GoogleAuthProvider();


// /// Sign in event handlers

// signInBtnStudent.onclick = () => auth.signInWithPopup(provider);
// signInBtnAdvisor.onclick = () => auth.signInWithPopup(provider);


// // signInBtnAdvisor.addEventListener("click", function () {
// //     // Redirect the user to page2.html when button 2 is clicked
// //     auth.signOut();
// //     whenSignedIn.hidden = true;
// //     whenSignedOut.hidden = false;


// // });

// signOutBtn.onclick = () => auth.signOut();

// auth.onAuthStateChanged(user => {
//     if (user) {
//         // signed in
//         whenSignedIn.hidden = false;
//         whenSignedOut.hidden = true;
//         // redicrect to 
//         userDetails.innerHTML = `<h3>Hello ${user.displayName}!</h3> <p>User ID: ${user.uid}</p>`;

//         // var studentPanel = document.getElementById("signInBtnStudent");
//         // var advisorPanel = document.getElementById("signInBtnAdvisor");

//     } else {
//         // not signed in
//         whenSignedIn.hidden = true;
//         whenSignedOut.hidden = false;
//         userDetails.innerHTML = '';
//     }
// });



// ///// Firestore /////

// const db = firebase.firestore();

// const createThing = document.getElementById('createThing');
// const thingsList = document.getElementById('thingsList');


// let thingsRef;
// let unsubscribe;

// auth.onAuthStateChanged(user => {

//     if (user) {

//         // Database Reference
//         thingsRef = db.collection('things')

//         createThing.onclick = () => {

//             const { serverTimestamp } = firebase.firestore.FieldValue;

//             thingsRef.add({
//                 uid: user.uid,
//                 name: faker.commerce.productName(),
//                 createdAt: serverTimestamp()
//             });
//         }


//         // Query
//         unsubscribe = thingsRef
//             .where('uid', '==', user.uid)
//             .orderBy('createdAt') // Requires a query
//             .onSnapshot(querySnapshot => {

//                 // Map results to an array of li elements

//                 const items = querySnapshot.docs.map(doc => {

//                     return `<li>${doc.data().name}</li>`

//                 });

//                 thingsList.innerHTML = items.join('');

//             });



//     } else {
//         // Unsubscribe when the user signs out
//         unsubscribe && unsubscribe();
//     }
// });





// // const auth = firebase.auth(); // auth SDK

// // const whenSignedIn = document.getElementById("whenSignedIn");
// // const whenSignedOut = document.getElementById("whenSignedOut");


// // const signInBtn = document.getElementById("signInBtn");
// // const signOutBtn = document.getElementById("signOutBtn");

// // const userDetails = document.getElementById("userDetails");

// // const provider = new firebase.auth.GoogleAuthProvider();

// // signInBtn.onclick = () => auth.signInWithPopup(provider);

// // signOutBtn.onclick = () => auth.signOut();


// // // auth.onAuthStateChanged(user => {
// // //     if (user) {
// // //         // signed in
// // //     } else {
// // //         // not signed in 
// // //     }

// // // });