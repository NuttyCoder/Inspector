import SwiftUI

struct ContentView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var loginSuccess: Bool = false

    var body: some View {
        NavigationView {
            VStack {
                Text("Login")
                    .font(.largeTitle)
                    .padding()

                TextField("Username", text: $username)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

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
            }
            .padding()
        }
    }

    func authenticateUser(username: String, password: String) {
        // Here you would typically call a backend service to verify credentials.
        // For simplicity, we'll just check if both fields are non-empty.
        if !username.isEmpty && !password.isEmpty {
            loginSuccess = true
        } else {
            loginSuccess = false
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
