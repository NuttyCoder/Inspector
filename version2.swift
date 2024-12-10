import SwiftUI

struct ContentView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var loginSuccess: Bool = false
    @State private var showAlert: Bool = false

    var body: some View {
        NavigationView {
            VStack {
                Spacer()
                Text("Login")
                    .font(.largeTitle)
                    .padding()

                TextField("Username", text: $username)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                    .autocapitalization(.none)

                SecureField("Password", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                Button(action: {
                    authenticateUser(username: username, password: password)
                }) {
                    Text("Login")
                        .font(.headline)
                        .foregroundColor(.white)
                        .padding()
                        .frame(width: 220, height: 60)
                        .background(Color.blue)
                        .cornerRadius(15.0)
                }
                .padding()

                if loginSuccess {
                    Text("Login Successful!")
                        .foregroundColor(.green)
                        .padding()
                }

                Spacer()
            }
            .padding()
            .alert(isPresented: $showAlert) {
                Alert(title: Text("Invalid Input"), message: Text("Please enter both username and password"), dismissButton: .default(Text("OK")))
            }
        }
    }

    func authenticateUser(username: String, password: String) {
        if !username.isEmpty && !password.isEmpty {
            loginSuccess = true
            showAlert = false
        } else {
            loginSuccess = false
            showAlert = true
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
