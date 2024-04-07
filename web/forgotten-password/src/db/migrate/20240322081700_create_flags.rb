class CreateFlags < ActiveRecord::Migration[7.1]
  def change
    create_table :flags do |t|
      t.string :value

      t.timestamps
    end
  end
end
