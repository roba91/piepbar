# this goes to: FSIntra2013/lib/tasks/sample_data.rake
# may be used with: rake db:populate
# or with: rake db:drop db:create db:migrate db:populate

namespace :db do
    desc "Fill database with sample data"
    task populate: :environment do
        # no1
        User.create!(
            city: 'Kaiserslautern',
            on_beverage_list: true,
            loginname: 'f_walk09'
        )

        # no2
        User.create!(
            city: 'Kaiserslautern',
            on_beverage_list: true,
            loginname: 's_wolff09'
        )

        # no3
        # User.create!(
        #     firstname: "first",
        #     lastname: "last",
        #     email: "mail",
        #     city: 'Kaiserslautern'
        # )

        # stuff
        Beverage.create!( name: 'Wasser', capacity: 0.7, price: 0.4, available: true )
        Beverage.create!( name: 'Spezi', capacity: 0.5, price: 0.6, available: true )
        Beverage.create!( name: 'Cola', capacity: 0.5, price: 0.7, available: true )
        Beverage.create!( name: 'Apfelsaftschorle', capacity: 0.7, price: 0.7, available: true )
        Beverage.create!( name: 'Bier', capacity: 0.5, price: 0.85, available: true )
        Beverage.create!( name: 'Mate', capacity: 0.5, price: 1.0, available: true )
        Beverage.create!( name: 'Mate Cola', capacity: 0.5, price: 0.9, available: true )
        Beverage.create!( name: 'Braumeister 0.33', capacity: 0.33, price: 0.8, available: true )
        Beverage.create!( name: 'Braumeister', capacity: 0.5, price: 0.9, available: true )
    end
end