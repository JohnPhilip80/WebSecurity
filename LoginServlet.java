package edu.cca.john.banking.servlet1;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.sql.*;
import java.util.UUID;

import edu.cca.john.banking.util1.DBConnection;
@WebServlet("/LoginServlet")
public class LoginServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String username = request.getParameter("username");
        String password = request.getParameter("password");

        try (Connection con = DBConnection.getConnection()) {

            PreparedStatement ps = con.prepareStatement(
                "SELECT * FROM users WHERE login_name=? AND login_password=?"
            );
            ps.setString(1, username);
            ps.setString(2, password);

            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                Long userId = rs.getLong("user_id");
                

                // Generate session ID
                String sessionId = UUID.randomUUID().toString();

                // Store session in DB
                PreparedStatement sessionPs = con.prepareStatement(
                    "INSERT INTO sessions(session_id, user_id) VALUES (?, ?)"
                );
                sessionPs.setString(1, sessionId);
                sessionPs.setLong(2, userId);
                sessionPs.executeUpdate();

                // Set session ID in cookie
                Cookie cookie = new Cookie("SESSION_ID", sessionId);
                response.addCookie(cookie);

                response.sendRedirect("dashboard.jsp");

            } else {
                response.getWriter().println("Invalid credentials");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}