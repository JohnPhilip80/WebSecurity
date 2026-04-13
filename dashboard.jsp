<%@ page import="java.sql.*,edu.cca.john.banking.util1.DBConnection" %>
<%
    String sessionId = null;
	String userName = null;
	Long balance = null;
	
    Cookie[] cookies = request.getCookies();
    if (cookies != null) {
        for (Cookie c : cookies) {
            if (c.getName().equals("SESSION_ID")) {
                sessionId = c.getValue();
            }
        }
    }

    boolean validSession = false;

    if (sessionId != null) {
        try {
            Connection con = DBConnection.getConnection();
            PreparedStatement ps = con.prepareStatement(
                "SELECT a.login_name, b.balance_amount FROM sessions c INNER JOIN users a ON c.user_id = a.user_id INNER JOIN accounts b ON c.user_id = b.user_id WHERE c.session_id=?"
            );
            ps.setString(1, sessionId);

            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                validSession = true;
                userName = rs.getString(1);
                balance = rs.getLong(2);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /*if (!validSession) {
        response.sendRedirect("login.jsp");
        return;
    }*/
%>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h2>Welcome <%= userName %> to Dashboard</h2>
    <h2>Your Balance Amount: <%= balance %></h2>
    <a href="LogoutServlet">Logout</a>
</body>
</html>