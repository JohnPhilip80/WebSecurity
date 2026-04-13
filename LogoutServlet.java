package edu.cca.john.banking.servlet1;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.sql.*;

import edu.cca.john.banking.util1.DBConnection;
@WebServlet("/LogoutServlet")
public class LogoutServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String sessionId = null;

        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if (c.getName().equals("SESSION_ID")) {
                    sessionId = c.getValue();
                }
            }
        }

        if (sessionId != null) {
            try (Connection con = DBConnection.getConnection()) {

                PreparedStatement ps = con.prepareStatement(
                    "DELETE FROM sessions WHERE session_id=?"
                );
                ps.setString(1, sessionId);
                ps.executeUpdate();

            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        // Remove cookie
        Cookie cookie = new Cookie("SESSION_ID", "");
        cookie.setMaxAge(0);
        response.addCookie(cookie);

        response.sendRedirect("login.jsp");
    }
}